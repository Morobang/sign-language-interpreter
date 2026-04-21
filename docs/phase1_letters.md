# Phase 1 — Letters

**Goal:** Get the full pipeline working end to end on letters A–Z before touching words.

---

## Why letters first?

Words are harder than letters because:
- A letter is a **static** hand position — one frame is enough
- A word is a **motion** — it happens across multiple frames over time
- If we can't get letters working, words have no chance

Letters let us prove the whole pipeline works cheaply and quickly. Once a letter classifier works live on camera, we know every piece is connected correctly. Then we upgrade.

---

## The pipeline for letters

```
ASL Alphabet image
       ↓
MediaPipe extracts 21 landmarks (63 numbers)
       ↓
Save to CSV: [x1,y1,z1, x2,y2,z2, ... x21,y21,z21, label]
       ↓
Train Random Forest on that CSV
       ↓
Live camera: extract landmarks from each frame → predict → show on screen
```

---

## Steps

### Step 1 — 02_mediapipe_test.ipynb ← you are here
Test that MediaPipe can detect a hand from one ASL Alphabet image and give back 21 landmarks. Just one image. If this doesn't work, stop and fix it before moving on.

**What success looks like:**
- Image displays with dots drawn on each finger joint
- You can print the 63 landmark values (x, y, z for each of 21 points)

---

### Step 2 — 03_extract_landmarks.ipynb
Loop MediaPipe over every image in the ASL Alphabet dataset (~87,000 images). For each image, extract the 63 landmark values and save them with the label into a CSV. This CSV is your real training data.

**What success looks like:**
- A file `data/processed/landmarks.csv` exists
- It has 64 columns (63 landmarks + 1 label)
- It has close to 87,000 rows

---

### Step 3 — 04_train_letters.ipynb
Load `landmarks.csv`, split into train/test, train a Random Forest classifier, evaluate accuracy. Expect 90%+ accuracy if MediaPipe extraction went well.

**What success looks like:**
- Accuracy above 90% on test set
- Confusion matrix shows which letters get confused with each other
- Model saved to `models/letter_model.pkl`

---

### Step 4 — src/run.py
Open camera, run MediaPipe on each frame, feed landmarks into the saved model, show the predicted letter on screen. This is the first real working demo.

**What success looks like:**
- You sign "A" and "A" appears on screen
- Prediction updates in real time as you change signs

---

## Key concept — why landmarks and not raw images?

You could train directly on the raw 200x200 photos from the ASL Alphabet dataset. But that has problems:
- Raw images are affected by lighting, skin tone, background, camera quality
- A model trained on studio photos will fail on your webcam

Landmarks solve this — MediaPipe gives you the **shape of the hand** as relative coordinates. It doesn't matter if your room is dark or bright, or what your skin tone is. The 63 numbers describe the geometry of your hand, not the pixels of a photo. That's why this approach generalises to real cameras.
