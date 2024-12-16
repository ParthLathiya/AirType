import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
from collections import deque
import numpy as np
from pynput.keyboard import Controller, Key
from time import sleep, time

# Initialize video capture
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Initialize HandDetector for hand tracking
detector = HandDetector(detectionCon=0.8, minTrackCon=0.5)

# Initialize virtual keyboard controller
keyboard = Controller()

# Define virtual keyboard layout
keyboard_keys = [
    ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"],
    ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
    ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
    ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"],
    ["SPACE", "ENTER", "BACKSPACE"]
]

class Button:
    def __init__(self, pos, text, size=(85, 85)):
        self.pos = pos
        self.size = size
        self.text = text
        self.last_pressed_time = 0

def draw_buttons(img, button_list):
    overlay = img.copy()
    alpha = 0.6  # Transparency factor
    for button in button_list:
        x, y = button.pos
        w, h = button.size
        cv2.rectangle(overlay, button.pos, (int(x + w), int(y + h)),
                      (255, 255, 255), cv2.FILLED)
        cv2.putText(overlay, button.text, (x + 20, y + 65),
                    cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 0), 4)
    img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)
    return img

# Create Button objects for keyboard
button_list = []
for k in range(len(keyboard_keys)):
    for x, key in enumerate(keyboard_keys[k]):
        if key not in ["SPACE", "ENTER", "BACKSPACE"]:
            button_list.append(Button((100 * x + 25, 100 * k + 50), key))
        elif key == "ENTER":
            button_list.append(Button((100 * x - 30, 100 * k + 50), key, (220, 85)))
        elif key == "SPACE":
            button_list.append(Button((100 * x + 780, 100 * k + 50), key, (220, 85)))
        elif key == "BACKSPACE":
            button_list.append(Button((100 * x + 140, 100 * k + 50), key, (400, 85)))

# Define Air Canvas components
bpoints = [deque(maxlen=1024)]
gpoints = [deque(maxlen=1024)]
rpoints = [deque(maxlen=1024)]
ypoints = [deque(maxlen=1024)]
blue_index, green_index, red_index, yellow_index = 0, 0, 0, 0

colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]
colorIndex = 0

# Setup canvas
paintWindow = np.zeros((471, 636, 3), dtype=np.uint8) + 255
cv2.namedWindow('Canvas', cv2.WINDOW_NORMAL)

# Cooldown for key press
cooldown_time = 0.5

# Mode variables
mode = 'Canvas'  # Start in Canvas mode
switch_gesture_cooldown = 1.0  # Cooldown between switching modes
last_switch_time = 0

# Function to check if all fingers are extended (open palm)
def is_open_palm(lm_list):
    if len(lm_list) == 0:
        return False
    # Check thumb
    thumb_is_open = lm_list[4][0] > lm_list[3][0]  # Check if thumb is far from the palm
    # Check fingers (index to pinky)
    fingers_are_open = [
        lm_list[8][1] < lm_list[6][1],  # Index finger
        lm_list[12][1] < lm_list[10][1],  # Middle finger
        lm_list[16][1] < lm_list[14][1],  # Ring finger
        lm_list[20][1] < lm_list[18][1]   # Pinky finger
    ]
    return thumb_is_open and all(fingers_are_open)

while True:
    # Read webcam frame
    success, img = cap.read()
    img = cv2.flip(img, 1)  # Mirror the frame for natural interaction

    # Detect hands and landmarks
    allHands, img = detector.findHands(img)

    if len(allHands) == 0:
        lm_list, bbox_info = [], []
    else:
        # Get hand landmark list and bounding box info
        lm_list, bbox_info = allHands[0]['lmList'], allHands[0]['bbox']

    # Draw canvas or keyboard based on the current mode
    if mode == 'Canvas':
        # Air Canvas Mode
        img = cv2.rectangle(img, (40, 1), (140, 65), (0, 0, 0), 2)
        img = cv2.rectangle(img, (160, 1), (255, 65), (255, 0, 0), 2)
        img = cv2.rectangle(img, (275, 1), (370, 65), (0, 255, 0), 2)
        img = cv2.rectangle(img, (390, 1), (485, 65), (0, 0, 255), 2)
        img = cv2.rectangle(img, (505, 1), (600, 65), (0, 255, 255), 2)
        cv2.putText(img, "CLEAR", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(img, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(img, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(img, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(img, "YELLOW", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)

        # Simultaneously display camera and canvas
        cv2.imshow("Canvas", paintWindow)

        # Code to detect index finger and draw lines on the canvas...
        # Example: Detect index finger and draw
        if lm_list:
            fore_finger = (lm_list[8][0], lm_list[8][1])
            thumb = (lm_list[4][0], lm_list[4][1])

            # Draw lines on the canvas and update points
            if fore_finger[1] <= 65:  # Color or Clear Selection
                if 40 <= fore_finger[0] <= 140:  # Clear button
                    bpoints, gpoints, rpoints, ypoints = [deque(maxlen=1024)], [deque(maxlen=1024)], [deque(maxlen=1024)], [deque(maxlen=1024)]
                    blue_index, green_index, red_index, yellow_index = 0, 0, 0, 0
                    paintWindow[67:, :, :] = 255
                elif 160 <= fore_finger[0] <= 255:
                    colorIndex = 0  # Blue
                elif 275 <= fore_finger[0] <= 370:
                    colorIndex = 1  # Green
                elif 390 <= fore_finger[0] <= 485:
                    colorIndex = 2  # Red
                elif 505 <= fore_finger[0] <= 600:
                    colorIndex = 3  # Yellow

            else:
                if colorIndex == 0:
                    bpoints[blue_index].appendleft(fore_finger)
                elif colorIndex == 1:
                    gpoints[green_index].appendleft(fore_finger)
                elif colorIndex == 2:
                    rpoints[red_index].appendleft(fore_finger)
                elif colorIndex == 3:
                    ypoints[yellow_index].appendleft(fore_finger)

            # Draw the points on the canvas
            points = [bpoints, gpoints, rpoints, ypoints]
            for i in range(len(points)):
                for j in range(len(points[i])):
                    for k in range(1, len(points[i][j])):
                        if points[i][j][k - 1] is None or points[i][j][k] is None:
                            continue
                        cv2.line(paintWindow, points[i][j][k - 1], points[i][j][k], colors[i], 2)

    elif mode == 'Keyboard':
        # Virtual Keyboard Mode
        img = draw_buttons(img, button_list)

        # Detect key presses and highlight on the keyboard
        if lm_list:
            for button in button_list:
                x, y = button.pos
                w, h = button.size

                # Check if index finger (lmList[8]) is within the button bounds
                if x < lm_list[8][0] < x + w and y < lm_list[8][1] < y + h:
                    overlay = img.copy()
                    cv2.rectangle(overlay, button.pos, (x + w, y + h),
                                  (247, 45, 134), cv2.FILLED)  # Highlight the button on hover
                    cv2.putText(overlay, button.text, (x + 20, y + 65),
                                cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 0), 4)
                    img = cv2.addWeighted(overlay, 0.6, img, 1 - 0.6, 0)

                    # Calculate distance between thumb (lmList[4]) and index finger (lmList[8])
                    distance = np.sqrt((lm_list[8][0] - lm_list[4][0])**2 + (lm_list[8][1] - lm_list[4][1])**2)

                    # If distance is small and cooldown has passed, simulate key press
                    if distance < 30 and time() - button.last_pressed_time > cooldown_time:
                        button.last_pressed_time = time()  # Update the last pressed time

                        # Check for special keys
                        if button.text not in ['ENTER', "BACKSPACE", "SPACE"]:
                            keyboard.press(button.text)  # Press the key
                            sleep(0.1)  # Small delay for better usability & prevent accidental key presses
                        else:
                            if button.text == "SPACE":
                                keyboard.press(Key.space)
                                keyboard.release(Key.space)
                                sleep(0.1)
                            elif button.text == "ENTER":
                                keyboard.press(Key.enter)
                                keyboard.release(Key.enter)
                                sleep(0.1)
                            elif button.text == "BACKSPACE":
                                keyboard.press(Key.backspace)
                                keyboard.release(Key.backspace)
                                sleep(0.1)

    # Show the camera feed with either canvas or keyboard overlay
    cv2.imshow("Virtual Interaction", img)

    # Check for open palm gesture to switch between modes
    if lm_list and time() - last_switch_time > switch_gesture_cooldown:
        if is_open_palm(lm_list):
            # Toggle mode
            if mode == 'Canvas':
                mode = 'Keyboard'
            else:
                mode = 'Canvas'
            last_switch_time = time()

    # Exit the application on pressing the ESC key
    if cv2.waitKey(1) & 0xFF == 27:
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
