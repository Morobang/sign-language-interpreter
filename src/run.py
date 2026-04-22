import cv2
import mediapipe as mp
import numpy as np
import pickle
import time
import os
import urllib.request

# ── Load model and label encoder ──────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(BASE_DIR, 'models', 'letter_model.pkl'), 'rb') as f:
    model = pickle.load(f)

with open(os.path.join(BASE_DIR, 'models', 'label_encoder.pkl'), 'rb') as f:
    le = pickle.load(f)

# ── Download hand landmarker model if not present ─────────────────────────────
LANDMARKER_PATH = os.path.join(BASE_DIR, 'models', 'hand_landmarker.task')

if not os.path.exists(LANDMARKER_PATH):
    print("Downloading hand_landmarker.task ...")
    urllib.request.urlretrieve(
        "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task",
        LANDMARKER_PATH
    )
    print("Downloaded.")

# ── MediaPipe Tasks setup ─────────────────────────────────────────────────────
BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=LANDMARKER_PATH),
    running_mode=VisionRunningMode.IMAGE,
    num_hands=1,
    min_hand_detection_confidence=0.7,
    min_tracking_confidence=0.5
)

landmarker = HandLandmarker.create_from_options(options)

# ── Drawing landmarks manually with OpenCV ────────────────────────────────────
HAND_CONNECTIONS = [
    (0,1),(1,2),(2,3),(3,4),
    (0,5),(5,6),(6,7),(7,8),
    (0,9),(9,10),(10,11),(11,12),
    (0,13),(13,14),(14,15),(15,16),
    (0,17),(17,18),(18,19),(19,20),
    (5,9),(9,13),(13,17)
]

def draw_landmarks_on_frame(frame, hand_landmarks_list):
    h, w = frame.shape[:2]
    for hand_landmarks in hand_landmarks_list:
        for a, b in HAND_CONNECTIONS:
            x1 = int(hand_landmarks[a].x * w)
            y1 = int(hand_landmarks[a].y * h)
            x2 = int(hand_landmarks[b].x * w)
            y2 = int(hand_landmarks[b].y * h)
            cv2.line(frame, (x1, y1), (x2, y2), (0, 200, 255), 2)
        for lm in hand_landmarks:
            cx = int(lm.x * w)
            cy = int(lm.y * h)
            cv2.circle(frame, (cx, cy), 5, (0, 255, 100), -1)

# ── Camera setup ──────────────────────────────────────────────────────────────
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Camera not found.")
    exit()

print("✅ Camera open — press Q to quit")

# ── State variables ───────────────────────────────────────────────────────────
prediction = "..."
confidence = 0.0
fps_time   = time.time()

# ── Main loop ─────────────────────────────────────────────────────────────────
while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Failed to read frame")
        break

    frame = cv2.flip(frame, 1)

    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img_rgb)

    result = landmarker.detect(mp_image)

    hand_detected = len(result.hand_landmarks) > 0

    if hand_detected:
        draw_landmarks_on_frame(frame, result.hand_landmarks)

        landmarks = []
        for lm in result.hand_landmarks[0]:
            landmarks.extend([lm.x, lm.y, lm.z])

        proba      = model.predict_proba([landmarks])[0]
        pred_idx   = np.argmax(proba)
        prediction = le.inverse_transform([pred_idx])[0]
        confidence = proba[pred_idx]

    fps      = 1 / (time.time() - fps_time)
    fps_time = time.time()

    cv2.rectangle(frame, (0, 0), (frame.shape[1], 100), (0, 0, 0), -1)

    cv2.putText(frame, prediction, (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 100), 4)

    cv2.putText(frame, f"Confidence: {confidence:.0%}", (200, 45),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (200, 200, 200), 2)

    cv2.putText(frame, f"FPS: {fps:.0f}", (10, frame.shape[0] - 15),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (150, 150, 150), 1)

    if not hand_detected:
        cv2.putText(frame, "No hand detected", (200, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (100, 100, 100), 2)

    cv2.imshow("Sign Language Interpreter — Phase 1 (Letters)", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ── Cleanup ───────────────────────────────────────────────────────────────────
cap.release()
cv2.destroyAllWindows()
landmarker.close()
print("Camera closed.")