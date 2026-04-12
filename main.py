import streamlit as st 
import cv2
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from mediapipe.python.solutions import hands as mp_hands_module
from mediapipe.python.solutions import drawing_utils as mp_drawing

# ---- Volume Setup ----
devices = AudioUtilities.GetSpeakers()
activate = devices._dev.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(activate, POINTER(IAudioEndpointVolume))

vol_range = volume.GetVolumeRange()
min_vol = vol_range[0]
max_vol = vol_range[1]

# ---- MediaPipe Setup ----
hands = mp_hands_module.Hands(max_num_hands=1, min_detection_confidence=0.7)

# ---- Camera Setup ----
cap = cv2.VideoCapture(0)

def get_distance(p1, p2):
    return np.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands_module.HAND_CONNECTIONS)

            h, w, _ = frame.shape

            thumb_tip = hand_landmarks.landmark[mp_hands_module.HandLandmark.THUMB_TIP]
            index_tip = hand_landmarks.landmark[mp_hands_module.HandLandmark.INDEX_FINGER_TIP]

            x1, y1 = int(thumb_tip.x * w), int(thumb_tip.y * h)
            x2, y2 = int(index_tip.x * w), int(index_tip.y * h)

            cv2.circle(frame, (x1, y1), 10, (255, 0, 0), cv2.FILLED)
            cv2.circle(frame, (x2, y2), 10, (255, 0, 0), cv2.FILLED)
            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)

            length = get_distance((x1, y1), (x2, y2))

            vol = np.interp(length, [30, 200], [min_vol, max_vol])
            vol_percent = np.interp(length, [30, 200], [0, 100])

            volume.SetMasterVolumeLevel(vol, None)

            cv2.putText(frame, f'Vol: {int(vol_percent)}%', (40, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            bar_x = 50
            bar_top = 100
            bar_bottom = 400
            bar_height = int(np.interp(vol_percent, [0, 100], [bar_bottom, bar_top]))
            cv2.rectangle(frame, (bar_x, bar_top), (bar_x + 30, bar_bottom), (200, 200, 200), 2)
            cv2.rectangle(frame, (bar_x, bar_height), (bar_x + 30, bar_bottom), (0, 255, 0), cv2.FILLED)

    cv2.imshow("Gesture Volume Control", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()