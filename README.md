# ✨ AirCanvas: Virtual Hand Gesture Drawing

## 🎨 Description
AirCanvas lets you paint virtually using hand gestures. No physical tools needed - just your hand and creativity!
## ⚡ Quick Features
- 🖌️ Draw in mid-air using hand gestures
- 🎨 Multiple color options (Blue, Green, Red, Yellow)
- 📏 Adjustable brush sizes
- 💫 Real-time hand tracking
- 🔄 Canvas clearing option
- 🖼️ Smooth drawing experience
- 📸 Live webcam integration

## 🛠️ Technical Requirements

### Hardware
- Webcam (Optional)
- Computer with Python support

### Software Dependencies
```bash
pip install opencv-python
pip install mediapipe
pip install numpy
```

## 🚀 Installation & Setup

1. Clone the repository
```bash
git clone https://github.com/Vinandra-Adam-Saputra/AirCanvas-VirtualDrawing.git
cd AirCanvas-VirtualDrawing
```

2. Install dependencies

3. Run the application
```bash
python virtual_paint.py
```

## 🎮 Controls & Usage

### Hand Gestures
- ☝️ **Index Finger Up + Middle Finger Down**: Activate drawing mode
- ✋ **Other Positions**: Pause drawing

### Keyboard Controls
- `q` - Quit application
- `c` - Clear canvas
- `b` - Switch to blue color
- `g` - Switch to green color
- `r` - Switch to red color
- `y` - Switch to yellow color
- `+` - Increase brush size
- `-` - Decrease brush size

## 💡 How It Works

### Hand Detection
- Uses MediaPipe Hands for accurate hand landmark detection
- Tracks 21 different points on your hand
- Focuses on index finger tip for drawing

### Drawing Logic
1. **Initialization**
   - Sets up video capture
   - Creates empty canvas
   - Initializes color options and brush settings

2. **Hand Tracking**
   - Detects hand in frame
   - Identifies finger positions
   - Determines drawing mode based on gesture

3. **Drawing Process**
   - Tracks index finger movement
   - Creates continuous lines when drawing
   - Maintains smooth line quality

## 🛠️ Customization

### Adjusting Detection Sensitivity
```python
self.hands = self.mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
```

### Adding New Colors
```python
self.colors = {
    'blue': (255, 0, 0),
    'green': (0, 255, 0),
    'red': (0, 0, 255),
    'yellow': (0, 255, 255)
    # Add your custom colors here
}
```


## 📷 Screenshoots
![WhatsApp Image 2025-02-02 at 19 17 37](https://github.com/user-attachments/assets/4113a7a0-1e6d-4b05-831e-dd3250996729)
![WhatsApp Image 2025-02-02 at 19 17 37 (1)](https://github.com/user-attachments/assets/bbd83e44-174c-440f-863d-12b4aaee5f16)
![WhatsApp Image 2025-02-02 at 19 17 38](https://github.com/user-attachments/assets/13289a23-950e-48bc-90c0-d4d6507ec942)


## 🤝 Contributing

1. Fork the repository
2. Create feature branch
```bash
git checkout -b feature/amazingfeature
```
3. Commit changes
```bash
git commit -m 'Add amazing feature'
```
4. Push to branch
```bash
git push origin feature/amazingfeature
```
5. Open a Pull Request

## 📜 License
This project is licensed under the [MIT License](LICENSE)

## 🙏 Acknowledgments
- MediaPipe team for hand detection
- OpenCV community
- All contributors and testers

---
