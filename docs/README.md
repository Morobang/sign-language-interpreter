# Sign Language Interpreter

A real-time sign language recognition system that uses your camera to detect hand signs and display the interpreted word or letter on screen — no video recording, no delays, frame by frame.

---

## The big picture

```
Camera → MediaPipe (hand landmarks) → Classifier (trained model) → Screen output
```

You point the camera at someone signing. MediaPipe finds their hand and gives you 21 keypoints (x, y, z coordinates for each finger joint = 63 numbers total). Those 63 numbers go into a trained model that predicts which sign it is. The result shows on screen in real time.

This is the same concept as YOLO object detection — except instead of drawing a box around a "cup", we're reading what the hand is saying.

---

## Datasets

| Dataset | What it covers | Used for |
|---|---|---|
| Sign Language MNIST | Letters A–Z as 28x28 pixel CSVs | Understanding the data format, quick experiments |
| ASL Alphabet (Kaggle) | Letters A–Z as real photos | Extracting landmarks, training letter classifier |
| WLASL Processed | 2000 words as video clips | Training word-level classifier (Phase 3) |

---

## Phases

### Phase 1 — Letters (where we are now)
Get the full pipeline working end to end on A–Z letters. Camera → landmarks → prediction → screen. This proves the system works before we tackle harder problems.

### Phase 2 — Your own words
Record yourself signing hello, thanks, yes, no, please using the collect script. Train on your own data. This works better than any dataset because it's your hand and your camera.

### Phase 3 — WLASL words
Use the 12,000 downloaded video clips to expand vocabulary to 100+ words. Harder because signs happen over time (motion), not in a single static frame.

---

## Project structure

```
sign-language-interpreter/
├── data/
│   ├── raw/                    # Original downloaded datasets — never modify these
│   │   ├── sign_mnist/
│   │   ├── asl_alphabet/
│   │   └── wlasl/
│   └── processed/              # Clean extracted features you generate
│       ├── landmarks/          # 63-number keypoint arrays from MediaPipe
│       └── labels.csv          # File → label mapping
├── notebooks/
│   ├── 01_explore_data.ipynb       ✅ done
│   ├── 02_mediapipe_test.ipynb     ← you are here
│   ├── 03_extract_landmarks.ipynb
│   ├── 04_train_letters.ipynb
│   └── 05_train_words.ipynb
├── src/
│   ├── collect_data.py         # Record your own signs via camera
│   ├── preprocess.py           # Extract landmarks from datasets
│   ├── train.py                # Train the classifier
│   └── run.py                  # Live camera inference
├── models/                     # Saved trained models
├── docs/                       # You are reading this
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Notebooks guide

| Notebook | Goal | Key question answered |
|---|---|---|
| 01_explore_data | Understand the datasets | What do we have? |
| 02_mediapipe_test | Test hand detection on one image | Can MediaPipe find a hand? |
| 03_extract_landmarks | Extract landmarks from full dataset | Can we turn images into 63 numbers? |
| 04_train_letters | Train and evaluate letter classifier | How accurate is the model? |
| 05_train_words | Train word-level classifier on WLASL | Can we recognise full words? |
