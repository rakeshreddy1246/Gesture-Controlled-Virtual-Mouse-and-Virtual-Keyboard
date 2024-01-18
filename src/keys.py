import cv2
import mediapipe as mp
import pyautogui
import time

KEYS = {
    "Q": (100, 100),
    "W": (200, 100),
    "E": (300, 100),
    "R": (400, 100),
    "T": (500, 100),
    "Y": (600, 100),
    "U": (700, 100),
    "I": (800, 100),
    "O": (900, 100),
    "P": (1000, 100),
    "A": (105, 200),
    "S": (205, 200),
    "D": (305, 200),
    "F": (405, 200),
    "G": (505, 200),
    "H": (605, 200),
    "J": (705, 200),
    "K": (805, 200),
    "L": (905, 200),
    "Z": (175, 300),
    "X": (275, 300),
    "C": (375, 300),
    "V": (475, 300),
    "B": (575, 300),
    "N": (675, 300),
    "M": (775, 300),
    "ESC": (450, 400),  # Added "ESC" key to stop the virtual keyboard
}
KEY_PRESS_DURATION = 1000  # Adjust this value to set the delay between key presses (in seconds)

def draw_keyboard(frame):
    for key, (x, y) in KEYS.items():
        cv2.rectangle(frame, (x - 20, y - 20), (x + 20, y + 20), (255, 0, 0), 2)
        cv2.putText(frame, key, (x - 10, y + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

def get_keyboard_key(finger_position):
    # Check which key the finger is pointing to
    for key, (x, y) in KEYS.items():
        if abs(finger_position[0] - x) < 20 and abs(finger_position[1] - y) < 20:
            return key
    return None

DEBOUNCE_DURATION = 6.5
def main():
    mp_drawing = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands

    cap = cv2.VideoCapture(0)

    key_last_pressed = None
    key_pressed = False
    last_key_press_time = time.time()
    double_click_duration = 5.5  # Adjust this value to set the duration between two clicks to detect double-click

    with mp_hands.Hands(
        min_detection_confidence=0.7, min_tracking_confidence=0.5
    ) as hands:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Convert the BGR frame to RGB
            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Process the frame with Mediapipe
            results = hands.process(image_rgb)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Get the position of the tip of the index finger
                    index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                    height, width, _ = frame.shape
                    x, y = int(index_finger_tip.x * width), int(index_finger_tip.y * height)

                    # Draw the keyboard on the frame
                    draw_keyboard(frame)

                    # Get the keyboard key based on the finger position
                    key = get_keyboard_key((x, y))

                    if key is not None:
                        # Display the key being pointed
                        cv2.putText(frame, f"Press {key}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                        cv2.imshow("Virtual Keyboard", frame)
                        cv2.waitKey(200)  # Display the key for 200 milliseconds

                        current_time = time.time()
                        if key == key_last_pressed and current_time - last_key_press_time < double_click_duration:
                            # Simulate double-click by pressing the keyboard key twice
                            pyautogui.press(key)
                            pyautogui.press(key)
                        else:
                            # Simulate single-click by pressing the keyboard key once
                            pyautogui.press(key)

                        last_key_press_time = current_time
                        key_last_pressed = key

            cv2.imshow("Virtual Keyboard", frame)

            if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()