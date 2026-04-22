import cv2
import mediapipe as mp
import numpy as np
import pickle
import time

# ── Load model and label encoder ──────────────────────────────────────────────
with open('../models/letter_model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('../models/label_encoder.pkl', 'rb') as f:
    le = pickle.load(f)

# ── MediaPipe setup ───────────────────────────────────────────────────────────
mp_hands = mp.solutions.hands
mp_draw  = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,    # False = video stream mode (faster)
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)

# ── Camera setup ──────────────────────────────────────────────────────────────
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Camera not found. Check your camera connection.")
    exit()

print("✅ Camera open — press Q to quit")

# ── State variables ───────────────────────────────────────────────────────────
prediction  = "..."
confidence  = 0.0
fps_time    = time.time()

# ── Main loop ─────────────────────────────────────────────────────────────────
while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Failed to read frame")
        break

    # Mirror the frame so it feels natural (like a mirror)
    frame = cv2.flip(frame, 1)

    # Convert to RGB for MediaPipe
    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    # ── If a hand is detected ─────────────────────────────────────────────────
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:

            # Draw the landmark skeleton on the frame
            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            # Extract 63 values
            landmarks = []
            for lm in hand_landmarks.landmark:
                landmarks.extend([lm.x, lm.y, lm.z])

            # Predict
            proba      = model.predict_proba([landmarks])[0]
            pred_idx   = np.argmax(proba)
            prediction = le.inverse_transform([pred_idx])[0]
            confidence = proba[pred_idx]

    # ── FPS counter ───────────────────────────────────────────────────────────
    fps      = 1 / (time.time() - fps_time)
    fps_time = time.time()

    # ── Overlay — prediction box ──────────────────────────────────────────────
    # Dark background bar at top
    cv2.rectangle(frame, (0, 0), (frame.shape[1], 100), (0, 0, 0), -1)

    # Predicted letter — big
    cv2.putText(
        frame, prediction,
        (20, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        3, (0, 255, 100), 4
    )

    # Confidence score
    cv2.putText(
        frame, f"Confidence: {confidence:.0%}",
        (200, 45),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8, (200, 200, 200), 2
    )

    # FPS — bottom left
    cv2.putText(
        frame, f"FPS: {fps:.0f}",
        (10, frame.shape[0] - 15),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6, (150, 150, 150), 1
    )

    # No hand message
    if not results.multi_hand_landmarks:
        cv2.putText(
            frame, "No hand detected",
            (200, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            1, (100, 100, 100), 2
        )

    # ── Show frame ────────────────────────────────────────────────────────────
    cv2.imshow("Sign Language Interpreter — Phase 1 (Letters)", frame)

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ── Cleanup ───────────────────────────────────────────────────────────────────
cap.release()
cv2.destroyAllWindows()
hands.close()
print("Camera closed.")