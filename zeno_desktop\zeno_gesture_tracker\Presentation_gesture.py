import cv2
import time
import numpy as np
import pyautogui
import mediapipe as mp

# MediaPipe Setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.75)
mp_drawing = mp.solutions.drawing_utils
cooldown = 0.8

# State variables
gesture_mode = True
last_gesture_time = 0
prev_x = None
prev_y = None
prev_action = None

def detect_gestures():
    global gesture_mode, last_gesture_time, prev_x, prev_y, prev_action

    cap = cv2.VideoCapture(0)

    while gesture_mode:
        ret, frame = cap.read()
        if not ret:
            continue

        frame = cv2.flip(frame, 1)
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(image_rgb)

        gesture = None
        current_time = time.time()

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                index = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                current_x = index.x
                current_y = index.y

                if prev_x is not None:
                    delta_x = current_x - prev_x

                    # Detect horizontal swipe to the right
                    if delta_x > 0.25:
                        gesture = "next-slide"

                prev_x = current_x
                prev_y = current_y

                if gesture and (gesture != prev_action or current_time - last_gesture_time > cooldown):
                    last_gesture_time = current_time
                    prev_action = gesture

                    if gesture == "next-slide":
                        print("[Zeno] 👉 Moving to next slide")
                        pyautogui.press("right")

        # Show the camera feed with landmarks
        cv2.imshow("Zeno Gesture Control", frame)

        # Quit on 'q' key press
        if cv2.waitKey(10) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    detect_gestures()

