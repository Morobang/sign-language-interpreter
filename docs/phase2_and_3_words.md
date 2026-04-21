# Phase 2 & 3 — Words

These phases come after Phase 1 (letters) is fully working on live camera.

---

# Phase 2 — Your own words

**Goal:** Recognise a small set of common words — hello, thanks, yes, no, please — using data you record yourself.

## Why record your own data?

WLASL has 12,000 videos but they were recorded by many different signers in different conditions. Your model will be running on YOUR camera in YOUR lighting. The best training data for that is you, signing into your own camera.

Recording 200 samples of each word takes about 20 minutes and will give you a model that works better on your setup than anything pre-trained.

## How it works — LSTM vs Random Forest

Words are different from letters because they involve **motion**. "Hello" is a wave. "Thank you" moves from chin outward. A single frame doesn't tell you which word is being signed — you need to see several frames in sequence.

This is why we use an LSTM (Long Short-Term Memory network) for words:

```
Frame 1 landmarks → 
Frame 2 landmarks →  LSTM  →  "hello"
Frame 3 landmarks →
...
Frame 30 landmarks →
```

The LSTM learns the pattern of how landmarks change over time for each word.

## Steps
1. Use `src/collect_data.py` to record yourself signing each word
2. Extract landmarks from each recorded video (same MediaPipe, but frame by frame)
3. Train an LSTM on the sequences
4. Test live on camera

---

# Phase 3 — WLASL (100+ words)

**Goal:** Expand vocabulary using the 12,000 downloaded WLASL video clips.

## What changes

Same approach as Phase 2 but at scale:
- 100 or 2000 words instead of 5
- Videos from many different signers (more robust model)
- Longer training time
- Need to handle class imbalance (some words have more videos than others)

## Realistic expectations

| Words | Training time | Expected accuracy |
|---|---|---|
| 5 (your own) | Minutes | 90%+ |
| 100 (WLASL100) | 30–60 min | 70–80% |
| 2000 (WLASL2000) | Hours, GPU recommended | 50–65% |

Start with WLASL100 (top 100 words). Getting 75% accuracy on 100 words is a genuinely impressive result and a strong portfolio project.

---

## The full journey

```
Phase 1: Letters A–Z (static, Random Forest)          ← build this first
    ↓
Phase 2: 5 words, your own data (motion, LSTM)        ← prove words work
    ↓
Phase 3: 100 words, WLASL dataset (scale up)          ← the real project
    ↓
Future:  Sentence building, punctuation, deployment   ← stretch goals
```

Don't skip phases. Each one teaches you something you need for the next.
