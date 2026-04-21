# Notebook 03 — Extract Landmarks

**What this notebook does:** Runs MediaPipe over every image in the ASL Alphabet dataset and saves the extracted landmarks into a clean CSV file.

**Why this matters:** The raw dataset is 87,000 photos. You can't train a model on raw photos for a live camera system — it won't generalise. You need to convert those photos into hand geometry (the 63 landmark numbers) first. This notebook does that conversion once, and saves the result so you never have to do it again.

---

## What goes in, what comes out

```
IN:  87,000 images like this →  [photo of hand signing "A"]
OUT: landmarks.csv like this →  0, 0.51, 0.82, 0.01, 0.48, 0.79, 0.02, ...
                                 ↑ label  ↑ x1   ↑ y1   ↑ z1   ↑ x2 ...
```

The output CSV has:
- 1 column for the label (which letter)
- 63 columns for the landmarks (x, y, z × 21 points)
- One row per image = ~87,000 rows

---

## Important — not every image will work

MediaPipe sometimes fails to detect a hand. This can happen when:
- The hand is at an unusual angle
- The image is blurry
- The hand is too close to the edge

When this happens, **skip that image** — don't save a row for it. A smaller clean dataset is better than a large noisy one.

You should expect to lose maybe 5–10% of images this way. That's normal.

---

## What success looks like

- File `data/processed/landmarks.csv` exists
- Shape is roughly (78,000–87,000 rows) × 64 columns
- No null/NaN values
- Labels are evenly distributed across all 26 letters

---

## After this notebook

Next is `04_train_letters.ipynb` — where you load this CSV and train the actual classifier.
