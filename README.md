# 🤟 Sign Language Interpreter

A real-time sign language recognition system that reads hand signs through your camera and displays the interpreted letter or word on screen — no video recording, no delays, processed frame by frame.

> Python · MediaPipe · OpenCV · scikit-learn · TensorFlow · WLASL Dataset

---

## Demo

```
Camera → MediaPipe (21 hand landmarks = 63 numbers) → Trained Model → Screen output
```

Point your camera at someone signing. MediaPipe detects the hand and extracts 21 keypoints. Those 63 numbers go into a trained model that predicts the sign. The result appears on screen instantly.

Three modes — switch live while the camera is open:

| Mode | Key | What it does |
|---|---|---|
| Letter | `L` | Recognises A–Z using Random Forest |
| Word (personal) | `W` | Recognises your recorded words using LSTM |
| WLASL 100 | `A` | Recognises 100 common ASL words using LSTM trained on WLASL dataset |

---

## Why landmarks and not raw images?

Training on raw photos fails on live cameras — a model trained on studio photos breaks under webcam lighting, different backgrounds, or different skin tones.

MediaPipe solves this by giving us the **geometry of the hand** as relative coordinates. Lighting, background, and skin tone don't matter. The 63 numbers describe the shape of the hand, not the appearance of the photo.

```
21 keypoints × 3 values (x, y, z) = 63 numbers per frame
```

---

## Models

### Letter model — Random Forest
- **Data:** ASL Alphabet dataset (87,000 images, A–Z)
- **Architecture:** Random Forest (100 trees)
- **Why:** Letters are static — one frame is enough. Random Forest is fast, accurate, and needs no GPU.
- **Result:** ~95% accuracy

### Word model (personal) — LSTM
- **Data:** Self-recorded using `src/collect_data.py`
- **Architecture:** LSTM(64) → LSTM(32) → Dense(64) → softmax
- **Why:** Words involve motion across frames. LSTM reads sequences over time.
- **Result:** 90%+ accuracy on personal signs

### WLASL model — LSTM
- **Data:** WLASL Processed dataset (12,000 video clips, 100 words)
- **Architecture:** LSTM(128) → LSTM(64) → Dense(128) → softmax
- **Evaluation metric:** Top-5 accuracy (industry standard for WLASL)
- **Result:** ~75% top-5 accuracy on 100 words

---

## Project Structure

```
sign-language-interpreter/
│
├── data/
│   ├── raw/                          # Original datasets (gitignored)
│   │   ├── sign_mnist/
│   │   ├── asl_alphabet/
│   │   └── wlasl/
│   └── processed/                    # Generated features (gitignored)
│       ├── landmarks.csv
│       └── wlasl/
│
├── notebooks/
│   ├── 01_explore_data.ipynb
│   ├── 02_mediapipe_test.ipynb
│   ├── 03_extract_landmarks.ipynb
│   ├── 04_train_letters.ipynb
│   ├── 05_train_words.ipynb
│   └── 05_wlasl_train.ipynb
│
├── src/
│   ├── collect_data.py
│   └── run.py
│
├── models/                           # Saved models (gitignored)
├── docs/
├── .gitignore
├── requirements.txt
└── README.md
```

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

| Dataset | Link |
|---|---|
| Sign Language MNIST | [Kaggle](https://www.kaggle.com/datasets/datamunge/sign-language-mnist) |
| ASL Alphabet | [Kaggle](https://www.kaggle.com/datasets/grassknoted/asl-alphabet) |
| WLASL Processed | [Kaggle](https://www.kaggle.com/datasets/risangbaskoro/wlasl-processed) |

Place them under `data/raw/` following the project structure above.

### 4. Run the notebooks in order

```
01_explore_data.ipynb       → understand what you have
02_mediapipe_test.ipynb     → confirm hand detection works
03_extract_landmarks.ipynb  → convert 87k images to landmark arrays
04_train_letters.ipynb      → train and save the letter model
05_train_words.ipynb        → train on your personal recorded signs
05_wlasl_train.ipynb        → train on WLASL 100 words
```

### 5. Record your own word signs
```bash
python src/collect_data.py
```

### 6. Run live
```bash
python src/run.py
```

---

## Controls

| Key | Action |
|---|---|
| `L` | Switch to letter mode |
| `W` | Switch to personal word mode |
| `A` | Switch to WLASL 100 mode |
| `C` | Clear the sentence |
| `Q` | Quit |

---

## Requirements

```
Python 3.8+
opencv-python
mediapipe
scikit-learn
tensorflow
numpy
pandas
matplotlib
seaborn
tqdm
jupyterlab
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
| OpenCV | Camera access and video processing |
| scikit-learn | Random Forest for letters |
| TensorFlow / Keras | LSTM for word recognition |
| NumPy / Pandas | Data handling |
| Matplotlib / Seaborn | Visualisation |
| Jupyter | Notebooks |

---

## Phases

| Phase | Goal | Status |
|---|---|---|
| 1 — Letters | A–Z recognition live on camera | ✅ Complete |
| 2 — Personal words | Your own recorded signs | ✅ Complete |
| 3 — WLASL 100 | 100 common ASL words | ✅ Complete |
| Future | Web app deployment | 📋 Planned |

---

## Acknowledgements

- [WLASL dataset](https://github.com/dxli94/WLASL) — Li et al., WACV 2020
- [MediaPipe Hands](https://google.github.io/mediapipe/solutions/hands) — Google
- ASL Alphabet and Sign Language MNIST — Kaggle community