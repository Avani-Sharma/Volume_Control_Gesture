import streamlit as st
import cv2
import numpy as np
import mediapipe as mp
import math

from streamlit_webrtc import webrtc_streamer, VideoTransformerBase

import comtypes
from ctypes import cast, POINTER
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL


# -------- AUDIO INIT (GLOBAL SAFE) --------
comtypes.CoInitialize()

speakers = AudioUtilities.GetSpeakers()

interface = speakers._dev.Activate(
    IAudioEndpointVolume._iid_,
    CLSCTX_ALL,
    None
)

volume = cast(interface, POINTER(IAudioEndpointVolume))


# -------- HAND TRACKING --------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)


class VideoTransformer(VideoTransformerBase):
    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        img = cv2.flip(img, 1)

        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        if results.multi_hand_landmarks:
            for hand in results.multi_hand_landmarks:

                h, w, _ = img.shape
                lm = []

                for p in hand.landmark:
                    lm.append((int(p.x * w), int(p.y * h)))

                if lm:
                    x1, y1 = lm[4]   # Thumb tip
                    x2, y2 = lm[8]   # Index finger tip

                    # Distance between thumb and index finger
                    length = math.hypot(x2 - x1, y2 - y1)

                    # Map distance to volume (0.0 to 1.0)
                    vol = np.interp(length, [20, 200], [0.0, 1.0])
                    volume.SetMasterVolumeLevelScalar(vol, None)

                    # Visual feedback
                    cv2.circle(img, (x1, y1), 10, (255, 0, 0), cv2.FILLED)
                    cv2.circle(img, (x2, y2), 10, (255, 0, 0), cv2.FILLED)
                    cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

                    vol_percent = int(vol * 100)
                    cv2.putText(img, f'Volume: {vol_percent}%', (20, 50),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        return img


st.title("🖐️ Volume Control Hand Gesture")
st.write("Control your system volume by adjusting the distance between your **THUMB** and **INDEX FINGER**.")

webrtc_streamer(
    key="gesture",
    video_processor_factory=VideoTransformer,
)