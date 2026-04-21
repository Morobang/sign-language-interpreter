# Notebook 04 — Train Letters

**What this notebook does:** Loads the landmarks CSV, trains a classifier, evaluates it, and saves the model.

**Why this matters:** This is where the machine actually learns. You're teaching it "when these 63 numbers look like this → it's the letter A, when they look like that → it's B" and so on for all 26 letters.

---

## The model — Random Forest

We're using a Random Forest classifier. Here's why:

- Works extremely well on tabular data (our 63 numbers are tabular)
- Trains in seconds on this dataset
- Gives you confidence scores (how sure is it?)
- Easy to interpret — you can see which landmarks matter most
- No GPU needed

Later when we move to words we'll use an LSTM because words happen over time (sequences of frames). But for static letter positions, Random Forest is the right tool.

---

## What success looks like

- Accuracy above 90% on the test set
- Confusion matrix shows the model is mostly correct
- The letters that get confused make sense (e.g. M and N look similar)
- Model saved to `models/letter_model.pkl`

---

## Key things to check

**Confusion matrix** — shows you which letters the model confuses with each other. Some letters look very similar in ASL (M, N, S, T). If those are confused, that's expected. If completely unrelated letters are confused, something is wrong with the data.

**Per-class accuracy** — some letters might score 99%, others 85%. Know which ones are weak before you test on camera.

**Feature importance** — Random Forest can tell you which of the 63 landmark values matter most for prediction. The fingertip positions (landmarks 4, 8, 12, 16, 20) usually dominate.

---

## After this notebook

Next is `src/run.py` — the live camera inference script. You load the saved model, open the camera, and test it for real.
