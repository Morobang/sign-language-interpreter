# Notebook 02 — MediaPipe Test

**What this notebook does:** Tests that MediaPipe can detect a hand from a single ASL Alphabet image and extract 21 landmarks.

**Why this matters:** MediaPipe is the engine that powers everything. If it can't find a hand in a clean studio photo, it definitely won't work on a live camera. We test it in isolation first before building anything on top of it.

---

## What is MediaPipe?

MediaPipe is a library by Google that can detect hands in images and video. When it finds a hand it gives you 21 keypoints — one for each finger joint, knuckle, and the wrist.

```
Each keypoint = (x, y, z)
21 keypoints × 3 values = 63 numbers total

These 63 numbers describe the shape and position of the hand.
```

The 21 points are:
- 0: Wrist
- 1–4: Thumb (base to tip)
- 5–8: Index finger (base to tip)
- 9–12: Middle finger (base to tip)
- 13–16: Ring finger (base to tip)
- 17–20: Pinky (base to tip)

---

## What success looks like

By the end of this notebook you should be able to:
1. Load one image from the ASL Alphabet dataset
2. Run MediaPipe on it
3. See the image with dots and lines drawn on the hand (landmark overlay)
4. Print the 63 raw numbers MediaPipe extracted

That's it. One image. One hand detected. 63 numbers printed.

---

## What failure looks like and how to fix it

| Problem | Likely cause | Fix |
|---|---|---|
| No landmarks detected | Image path wrong | Check the path, print it |
| No landmarks detected | Hand not visible in image | Try a different image |
| Import error on mediapipe | Not installed | `pip install mediapipe` |
| cv2 not found | Not installed | `pip install opencv-python` |
| Image shows black/blank | cv2 reads BGR, matplotlib needs RGB | Add `cv2.cvtColor(img, cv2.COLOR_BGR2RGB)` |

---

## After this notebook

Next is `03_extract_landmarks.ipynb` — where we run this same process on all 87,000 images and save the results to a CSV.
