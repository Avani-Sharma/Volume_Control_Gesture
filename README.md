<div align="center">
  <h1>🖐️ Gesture Volume Control</h1>
  <p>Control your system volume using hand gestures via webcam!</p>
</div>

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

---

## 🚀 How to Run

### 🖥️ Script Mode
```bash
py -3.10 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### 🌐 Streamlit Mode
```bash
py -3.10 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

---

## 🖐️ Gestures

| Gesture | Action |
|--------|--------|
| 👐 Fingers far apart | Volume Up |
| 🤏 Fingers close together | Volume Down |
| Q key | Quit *(Script mode only)* |

---

<div align="center">
  Made with ❤️ using Python, OpenCV, MediaPipe and Streamlit
</div>