import cv2
import threading
import time
import numpy as np
import pyautogui
import mediapipe as mp

# MediaPipe Setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.75)
mp_drawing = mp.solutions.drawing_utils

# State variables
gesture_mode = False
gesture_thread = None
last_gesture_time = 0
cooldown = 0.8
prev_action = None
prev_x = None
prev_y = None

def handle_gesture(gesture):
    if gesture == "tab":
        print("[Zeno] 🔁 Pressing Tab")
        pyautogui.press("tab")
    elif gesture == "scroll-down":
        print("[Zeno] ⬇️ Scrolling down")
        pyautogui.scroll(-500)
    elif gesture == "scroll-up":
        print("[Zeno] ⬆️ Scrolling up")
        pyautogui.scroll(500)

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

                thumb = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                index = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

                # Pinch (Tab)
                pinch_distance = np.linalg.norm(
                    np.array([thumb.x, thumb.y]) - np.array([index.x, index.y])
                )
                if pinch_distance < 0.04:
                    gesture = "tab"

                # Swipe detection
                current_x = index.x
                current_y = index.y

                if prev_x is not None and prev_y is not None:
                    delta_x = current_x - prev_x
                    delta_y = current_y - prev_y

                    # Horizontal swipe → scroll down
                    if abs(delta_x) > 0.25:
                        gesture = "scroll-down"
                    # Vertical swipe → scroll up
                    elif abs(delta_y) > 0.25:
                        gesture = "scroll-up"

                prev_x = current_x
                prev_y = current_y

                if gesture and (gesture != prev_action or current_time - last_gesture_time > cooldown):
                    last_gesture_time = current_time
                    prev_action = gesture
                    handle_gesture(gesture)

        # Removed this line 👇 to make it headless
        cv2.imshow("🖐 Zeno Gestures", frame)

        if cv2.waitKey(10) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

def start_gesture_mode():
    global gesture_mode, gesture_thread
    if not gesture_mode:
        print("[Zeno] 👀 Gesture tracking started. Press 'q' in the camera window to quit.")
        gesture_mode = True
        gesture_thread = threading.Thread(target=detect_gestures, daemon=True)
        gesture_thread.start()

def stop_gesture_mode():
    global gesture_mode
    print("[Zeno] 🛑 Gesture tracking stopped.")
    gesture_mode = False
    if gesture_thread is not None:
        gesture_thread.join()  # wait for thread to finish cleanly
        
# Main
if __name__ == "__main__":
    start_gesture_mode()

    # Keep the main thread alive until the gesture window is closed
    while gesture_mode:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            stop_gesture_mode()
            break






                
       