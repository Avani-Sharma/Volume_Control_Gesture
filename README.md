<div align="center">
  <h1>🖐️ Volume Control Gesture</h1>
  <p>Control your system volume using hand gestures via webcam!</p>
</div>

---

## 📌 Two Ways to Run

This project supports **two modes**:

| Mode | File | Interface |
|------|------|-----------|
| 🖥️ Script Mode | `main.py` | OpenCV window (terminal) |
| 🌐 Streamlit Mode | `app.py` | Web browser (Streamlit UI) |

---

## 💾 Requirements

```
opencv-python
mediapipe==0.10.9
comtypes
numpy
pycaw
streamlit
streamlit-webrtc
```

Install all dependencies:

```bash
pip install -r requirements.txt
```

---

## 🚀 How to Run

### 🖥️ Script Mode (`main.py`)

```bash
# Step 1 - Create virtual environment
py -3.10 -m venv .venv

# Step 2 - Activate
.venv\Scripts\activate

# Step 3 - Install libraries
pip install -r requirements.txt

# Step 4 - Run
python main.py
```

### 🌐 Streamlit Mode (`app.py`)

```bash
# Step 1 - Create virtual environment
py -3.10 -m venv .venv

# Step 2 - Activate
.venv\Scripts\activate

# Step 3 - Install libraries
pip install -r requirements.txt

# Step 4 - Run Streamlit app
streamlit run app.py
```

Then open your browser at `http://localhost:8501`

---

## 🖐️ Gestures

| Gesture | Action |
|--------|--------|
| 👐 Fingers far apart | Volume Up |
| 🤏 Fingers close together | Volume Down |
| Q key | Quit *(Script mode only)* |

---

## 📝 Code Explanation

### Importing Libraries

```python
import cv2
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from mediapipe.python.solutions import hands as mp_hands_module
from mediapipe.python.solutions import drawing_utils as mp_drawing
```

### Volume Control Setup using pycaw

```python
devices = AudioUtilities.GetSpeakers()
activate = devices._dev.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(activate, POINTER(IAudioEndpointVolume))
```

### Getting Volume Range

```python
vol_range = volume.GetVolumeRange()
min_vol = vol_range[0]
max_vol = vol_range[1]
```

### Setting up Webcam using OpenCV

```python
cap = cv2.VideoCapture(0)
```

### MediaPipe Hand Detection

```python
hands = mp_hands_module.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7)
```

### Getting Thumb and Index Finger Position

```python
thumb_tip = hand_landmarks.landmark[mp_hands_module.HandLandmark.THUMB_TIP]
index_tip = hand_landmarks.landmark[mp_hands_module.HandLandmark.INDEX_FINGER_TIP]
x1, y1 = int(thumb_tip.x * w), int(thumb_tip.y * h)
x2, y2 = int(index_tip.x * w), int(index_tip.y * h)
```

### Calculating Distance Between Fingers

```python
def get_distance(p1, p2):
    return np.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

length = get_distance((x1, y1), (x2, y2))
```

### Converting Distance to Volume using `numpy.interp()`

```python
vol = np.interp(length, [30, 200], [min_vol, max_vol])
vol_percent = np.interp(length, [30, 200], [0, 100])
```

### Setting System Volume

```python
volume.SetMasterVolumeLevel(vol, None)
```

### Streamlit WebRTC Integration (`app.py`)

The Streamlit version uses `streamlit-webrtc` to stream webcam frames directly in the browser.

```python
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase

class VideoTransformer(VideoTransformerBase):
    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        # Hand detection + volume control logic here
        return img

webrtc_streamer(key="gesture", video_processor_factory=VideoTransformer)
```

### Drawing Volume Bar *(Script mode)*

```python
cv2.rectangle(frame, (bar_x, bar_top), (bar_x + 30, bar_bottom), (200, 200, 200), 2)
cv2.rectangle(frame, (bar_x, bar_height), (bar_x + 30, bar_bottom), (0, 255, 0), cv2.FILLED)
```

### Displaying Output *(Script mode)*

```python
cv2.imshow("Gesture Volume Control", frame)
if cv2.waitKey(1) & 0xFF == ord('q'):
    break
```

---

<div align="center">
  Made with ❤️ using Python, OpenCV, MediaPipe and Streamlit
</div>