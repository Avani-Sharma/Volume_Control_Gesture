<div align="center">
  <h1>🖐️ Gesture Volume Control</h1>
  <p>Control your system volume using hand gestures via webcam!</p>
</div>

💾 Requirements: 
opencv-python
mediapipe==0.10.9
comtypes
numpy
pycaw

bashpip install -r requirements.txt

🚀 How to Run
bash
# Step 1 - Create virtual environment
py -3.10 -m venv .venv

# Step 2 - Activate
.venv\Scripts\activate

# Step 3 - Install libraries
pip install -r requirements.txt

# Step 4 - Run
python main.py

🖐️ Gestures
GestureAction👐 Fingers far apartVolume Up🤏 Fingers close togetherVolume DownQ keyQuit

📝 Code Explanation
Importing Libraries
pythonimport cv2
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from mediapipe.python.solutions import hands as mp_hands_module
from mediapipe.python.solutions import drawing_utils as mp_drawing

Volume Control Setup using pycaw
pythondevices = AudioUtilities.GetSpeakers()
activate = devices._dev.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(activate, POINTER(IAudioEndpointVolume))

Getting Volume Range
pythonvol_range = volume.GetVolumeRange()
min_vol = vol_range[0]
max_vol = vol_range[1]

Setting up Webcam using OpenCV
pythoncap = cv2.VideoCapture(0)

MediaPipe Hand Detection
pythonhands = mp_hands_module.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7)

Getting Thumb and Index Finger Position
pythonthumb_tip = hand_landmarks.landmark[mp_hands_module.HandLandmark.THUMB_TIP]
index_tip = hand_landmarks.landmark[mp_hands_module.HandLandmark.INDEX_FINGER_TIP]

x1, y1 = int(thumb_tip.x * w), int(thumb_tip.y * h)
x2, y2 = int(index_tip.x * w), int(index_tip.y * h)

Calculating Distance Between Fingers
pythondef get_distance(p1, p2):
    return np.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

length = get_distance((x1, y1), (x2, y2))

Converting Distance to Volume using numpy.interp()
pythonvol = np.interp(length, [30, 200], [min_vol, max_vol])
vol_percent = np.interp(length, [30, 200], [0, 100])

Setting System Volume
pythonvolume.SetMasterVolumeLevel(vol, None)

Drawing Volume Bar
pythoncv2.rectangle(frame, (bar_x, bar_top), (bar_x + 30, bar_bottom), (200, 200, 200), 2)
cv2.rectangle(frame, (bar_x, bar_height), (bar_x + 30, bar_bottom), (0, 255, 0), cv2.FILLED)

Displaying Output
pythoncv2.imshow("Gesture Volume Control", frame)
if cv2.waitKey(1) & 0xFF == ord('q'):
    break

<div align="center">
  Made with ❤️ using Python, OpenCV and MediaPipe
</div>