# 🤟 Sign Language Interpreter

A real-time sign language recognition system that reads hand signs through your camera and displays the interpreted letter or word on screen — no video recording, no delays, frame by frame.

> Built with Python, MediaPipe, OpenCV, and scikit-learn

---

## Demo

Point your camera at someone signing → landmarks are extracted from their hand → a trained model predicts the sign → the result appears on screen instantly.

```
Camera → MediaPipe (21 hand landmarks) → Classifier → Screen output
```

---

## Project Structure

```
sign-language-interpreter/
│
├── data/
│   ├── raw/                          # Original downloaded datasets (gitignored)
│   │   ├── sign_mnist/               # Sign Language MNIST — letters A–Z as CSVs
│   │   ├── asl_alphabet/             # ASL Alphabet — letters A–Z as images (87k photos)
│   │   └── wlasl/                    # WLASL — 12,000 word-level video clips
│   │       ├── WLASL_v0.3.json       # Metadata for all 2000 words
│   │       └── videos/               # Downloaded video clips
│   │
│   └── processed/                    # Clean extracted features (gitignored)
│       ├── landmarks.csv             # 63 MediaPipe values + label per image
│       └── labels.csv                # File → label mapping
│
├── notebooks/
│   ├── 01_explore_data.ipynb         # ✅ Understand the datasets
│   ├── 02_mediapipe_test.ipynb       # Test hand landmark detection
│   ├── 03_extract_landmarks.ipynb    # Extract landmarks from full dataset
│   ├── 04_train_letters.ipynb        # Train and evaluate letter classifier
│   └── 05_train_words.ipynb          # Train word-level classifier (WLASL)
│
├── src/
│   ├── collect_data.py               # Record your own signs via camera
│   ├── preprocess.py                 # Extract landmarks from image/video datasets
│   ├── train.py                      # Train the classifier
│   └── run.py                        # Live camera inference
│
├── models/                           # Saved trained models (gitignored)
│   ├── letter_model.pkl              # Random Forest for letters A–Z
│   └── word_model.pkl                # LSTM for word recognition
│
├── docs/                             # Phase guides and notebook explainers
│   ├── phase1_letters.md
│   ├── phase2_and_3_words.md
│   ├── 02_mediapipe_test.md
│   ├── 03_extract_landmarks.md
│   └── 04_train_letters.md
│
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Datasets

| Dataset | What it covers | Source |
|---|---|---|
| Sign Language MNIST | Letters A–Z as 28×28 pixel CSVs | [Kaggle](https://www.kaggle.com/datasets/datamunge/sign-language-mnist) |
| ASL Alphabet | Letters A–Z as real photos (87k images) | [Kaggle](https://www.kaggle.com/datasets/grassknoted/asl-alphabet) |
| WLASL Processed | 12,000 word-level ASL video clips | [Kaggle](https://www.kaggle.com/datasets/risangbaskoro/wlasl-processed) |

> Datasets are not included in this repo. Download them separately and place them under `data/raw/`.

---

## How It Works

### Why landmarks and not raw images?

Training on raw photos fails in real life — a model trained on studio photos breaks under webcam lighting or different backgrounds.

MediaPipe solves this by giving us the **geometry of the hand** as relative coordinates. It doesn't matter what your background looks like or how bright your room is. The 63 numbers describe the shape of your hand, not the pixels of a photo.

```
21 hand keypoints × 3 values (x, y, z) = 63 numbers per frame
```

### Letters (static signs)

```
Image → MediaPipe → 63 numbers → Random Forest → Letter prediction
```

Each letter is a static hand position so one frame is enough. Random Forest works excellently on this tabular data and trains in seconds.

### Words (motion signs)

```
Video frames → MediaPipe (per frame) → sequence of 63-number arrays → LSTM → Word prediction
```

Words involve movement over time. "Hello" is a wave, "thank you" moves from chin outward. An LSTM reads the sequence of landmark positions across frames and learns the motion pattern.

---

## Phases

### ✅ Phase 1 — Letters A–Z
Full pipeline working end to end: camera → landmarks → Random Forest → letter on screen.

### 🔄 Phase 2 — Your own words
Record yourself signing hello, thanks, yes, no, please. Train an LSTM on your own data. Faster and more accurate for your specific camera and lighting.

### 📋 Phase 3 — WLASL (100+ words)
Use the downloaded WLASL clips to scale up to 100 or 2000 words.

---

## Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/Morobang/sign-language-interpreter.git
cd sign-language-interpreter
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Download datasets
Download the three datasets from the Kaggle links above and place them in `data/raw/`.

### 4. Run the notebooks in order
```
01_explore_data.ipynb       → understand what you have
02_mediapipe_test.ipynb     → confirm hand detection works
03_extract_landmarks.ipynb  → convert images to 63-number arrays
04_train_letters.ipynb      → train and save the letter model
```

### 5. Run live inference
```bash
python src/run.py
```
Press `Q` to quit.

---

## Requirements

```
Python 3.8+
opencv-python
mediapipe
scikit-learn
numpy
pandas
matplotlib
seaborn
jupyterlab
tqdm
```

Install all:
```bash
pip install -r requirements.txt
```

---

## Tech Stack

| Tool | Purpose |
|---|---|
| MediaPipe | Hand landmark detection |
| OpenCV | Camera access and image processing |
| scikit-learn | Random Forest classifier (letters) |
| TensorFlow/Keras | LSTM model (words) |
| NumPy / Pandas | Data handling |
| Matplotlib / Seaborn | Visualisation |
| Jupyter | Experimentation and exploration |

---

## Acknowledgements

- [WLASL dataset](https://github.com/dxli94/WLASL) — Li et al., WACV 2020
- [MediaPipe](https://google.github.io/mediapipe/) — Google
- ASL Alphabet and Sign Language MNIST datasets via Kaggle