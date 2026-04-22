import cv2
import mediapipe as mp
import numpy as np
import os
import time

# ── Settings — change these to whatever words you want ────────────────────────
SIGNS           = ['hello', 'thanks', 'yes', 'no', 'please', 'sorry', 'help']
SAMPLES_PER_SIGN = 200      # how many samples to collect per word
SEQUENCE_LENGTH  = 30       # how many frames per sample (1 sample = 30 frames)
DATA_DIR         = '../data/raw/my_signs'

# ── MediaPipe setup ───────────────────────────────────────────────────────────
mp_hands = mp.solutions.hands
mp_draw  = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)

# ── Camera ────────────────────────────────────────────────────────────────────
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Camera not found")
    exit()

# ── Create folder structure ───────────────────────────────────────────────────
# data/raw/my_signs/
#   hello/
#     0.npy   ← sample 0 (30 frames × 63 values = array of shape 30,63)
#     1.npy   ← sample 1
#     ...
#   thanks/
#     0.npy
#     ...

for sign in SIGNS:
    os.makedirs(os.path.join(DATA_DIR, sign), exist_ok=True)

print(f"Collecting {SAMPLES_PER_SIGN} samples × {len(SIGNS)} signs")
print(f"Each sample = {SEQUENCE_LENGTH} frames of landmarks")
print(f"Saving to: {DATA_DIR}")

# ── Helper — draw status on frame ─────────────────────────────────────────────
def draw_status(frame, sign, sample_num, state, countdown=None):
    cv2.rectangle(frame, (0, 0), (frame.shape[1], 80), (0, 0, 0), -1)

    if state == 'waiting':
        msg = f"Next: '{sign.upper()}'  |  Sample {sample_num}/{SAMPLES_PER_SIGN}  |  Press SPACE to start"
        cv2.putText(frame, msg, (15, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 0), 2)

    elif state == 'countdown':
        msg = f"Get ready to sign '{sign.upper()}'...  {countdown}"
        cv2.putText(frame, msg, (15, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 200, 255), 2)

    elif state == 'recording':
        msg = f"RECORDING '{sign.upper()}'  —  Sample {sample_num}/{SAMPLES_PER_SIGN}"
        cv2.putText(frame, msg, (15, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 100), 2)
        # Red dot = recording indicator
        cv2.circle(frame, (frame.shape[1] - 30, 30), 12, (0, 0, 255), -1)

# ── Main collection loop ───────────────────────────────────────────────────────
for sign in SIGNS:
    print(f"\n── Collecting: {sign.upper()} ──")

    sample_num = 0

    while sample_num < SAMPLES_PER_SIGN:

        # ── WAITING STATE — wait for spacebar ─────────────────────────────────
        while True:
            ret, frame = cap.read()
            frame = cv2.flip(frame, 1)
            img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(img_rgb)

            if results.multi_hand_landmarks:
                for hl in results.multi_hand_landmarks:
                    mp_draw.draw_landmarks(frame, hl, mp_hands.HAND_CONNECTIONS)

            draw_status(frame, sign, sample_num + 1, 'waiting')
            cv2.imshow('Collect Sign Data', frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord(' '):     # spacebar = start this sample
                break
            if key == ord('q'):     # q = quit everything
                cap.release()
                cv2.destroyAllWindows()
                hands.close()
                print("Stopped early.")
                exit()

        # ── COUNTDOWN — 3 seconds to get into position ────────────────────────
        for count in [3, 2, 1]:
            countdown_start = time.time()
            while time.time() - countdown_start < 1:
                ret, frame = cap.read()
                frame = cv2.flip(frame, 1)
                img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = hands.process(img_rgb)

                if results.multi_hand_landmarks:
                    for hl in results.multi_hand_landmarks:
                        mp_draw.draw_landmarks(frame, hl, mp_hands.HAND_CONNECTIONS)

                draw_status(frame, sign, sample_num + 1, 'countdown', countdown=count)
                cv2.imshow('Collect Sign Data', frame)
                cv2.waitKey(1)

        # ── RECORDING — capture SEQUENCE_LENGTH frames ────────────────────────
        sequence = []   # will hold 30 arrays of 63 values each

        while len(sequence) < SEQUENCE_LENGTH:
            ret, frame = cap.read()
            frame = cv2.flip(frame, 1)
            img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(img_rgb)

            if results.multi_hand_landmarks:
                for hl in results.multi_hand_landmarks:
                    mp_draw.draw_landmarks(frame, hl, mp_hands.HAND_CONNECTIONS)

                    landmarks = []
                    for lm in hl.landmark:
                        landmarks.extend([lm.x, lm.y, lm.z])

                    sequence.append(landmarks)  # 63 values for this frame

            draw_status(frame, sign, sample_num + 1, 'recording')
            cv2.imshow('Collect Sign Data', frame)
            cv2.waitKey(1)

        # ── SAVE — only if we got a full sequence ──────────────────────────────
        if len(sequence) == SEQUENCE_LENGTH:
            save_path = os.path.join(DATA_DIR, sign, f'{sample_num}.npy')
            np.save(save_path, np.array(sequence))  # shape: (30, 63)
            sample_num += 1
            print(f"  Saved sample {sample_num}/{SAMPLES_PER_SIGN}")
        else:
            print(f"  ⚠ Skipped — hand lost during recording, try again")

print("\n✅ Data collection complete!")
print(f"Saved to: {DATA_DIR}")

cap.release()
cv2.destroyAllWindows()
hands.close()