# AirType: Virtual Keyboard with Hand Gesture Control

AirType is an innovative project that merges hand gesture recognition with a virtual keyboard interface. Using a webcam, users can interact with a dynamic virtual keyboard or an air canvas, enabling typing and drawing without physical contact. This project showcases a creative application of hand tracking technology for intuitive and futuristic human-computer interaction.

## Features

- **Gesture Recognition**: Detects hand movements and finger positions in real-time.
- **Virtual Keyboard**: Simulates keypresses on a virtual keyboard displayed on the screen.
- **Special Keys Support**: Includes `SPACE`, `ENTER`, and `BACKSPACE` functionality.
- **Air Canvas Mode**: Draw and create art by tracking finger movements in the air.
- **Interactive Feedback**: Highlights keys when hovered and provides visual cues for keypresses.
- **Mode Switching**: Seamlessly toggle between keyboard and canvas modes using an open palm gesture.

## Requirements

Install the following libraries to run the project:

```bash
pip install opencv-python cvzone numpy mediapipe pynput
```

## How It Works

### Keyboard Mode

1. **Hand Tracking**: Detects hand landmarks using the `cvzone` library and `MediaPipe` framework.
2. **Key Interaction**: Identifies index finger position to determine which key is being hovered over.
3. **Key Press Simulation**: Simulates pressing the hovered key when the thumb and index finger pinch.

### Canvas Mode

1. **Drawing**: Tracks finger movements to draw on a virtual canvas.
2. **Color Selection**: Switch between colors (Blue, Green, Red, Yellow) or clear the canvas with a gesture.
3. **Real-Time Visualization**: Displays the drawing alongside the live video feed for intuitive control.


## Usage

1. Clone the repository and navigate to the project directory.
2. Run the script:

   ```bash
   python virtual_keyboard.py
   ```

3. Use the virtual keyboard or draw on the air canvas:
   - **Keyboard Mode**: Hover over keys and pinch to press.
   - **Canvas Mode**: Select colors or draw freely by pointing with your index finger.
   - Switch between modes with an open palm gesture.

4. Exit the application by pressing the `ESC` key.

## Keyboard Layout

```
1  2  3  4  5  6  7  8  9  0
Q  W  E  R  T  Y  U  I  O  P
A  S  D  F  G  H  J  K  L  ;
Z  X  C  V  B  N  M  ,  .  /
[SPACE] [ENTER] [BACKSPACE]
```


## Limitations

- Requires a high-resolution webcam for optimal performance.
- Performs best in well-lit environments to ensure accurate gesture detection.
- May have difficulty distinguishing between unintended gestures or multiple hands.

## Future Enhancements

- Add support for multi-hand interaction.
- Improve gesture recognition for smoother and more diverse interactions.
- Include additional gestures for functionalities like copy, paste, or undo.
- Enhance the visual interface with customizable themes.

## Author

Parth Lathiya
