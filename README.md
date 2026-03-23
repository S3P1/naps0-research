# Naps0 — On-Device Infant Cry Classification

> Real-time, privacy-first baby cry monitor for Android.
> Classifies infant crying into four categories — **pain · hunger · discomfort · tired** — entirely on-device, with no cloud, no data upload, and no subscription.

---

## What it does

Naps0 listens continuously to a baby's cry and classifies the underlying need in real time. The entire inference pipeline runs on the Android device — no audio is ever transmitted to any server.

**Input:** continuous microphone stream (16 kHz)
**Output:** differentiated push notification per class, with onset latency under 100ms

---

## Architecture

The system uses a hierarchical two-stage pipeline:

```
Audio stream (mic)
    ↓
BurstEpisodeDetector (RMS energy + YIN pitch, PITCH_FMIN=160Hz)
    ↓  ≥2 bursts, ≥3s duration
Model A — binary pain/no-pain classifier (4ch, ONNX)
    ↓  pain ≥ 0.55 → immediate pain alert
CNN — hunger / discomfort / tired classifier (7ch, ONNX)
    ↓
EMA temporal smoothing (α=0.35) + alert cooldown (8s)
    ↓
Differentiated push notification per class
```

**Stage 1 (Model A):** Binary pain/no-pain classifier. Hierarchical separation ensures pain is never confused with other classes. pain_recall = 1.000 on validation set.

**Stage 2 (CNN):** MobileNetV2-based classifier for hunger, discomfort, and tired. Input: 7-channel spectrogram (Log-Mel + MFCC + Δ1 + Δ2 + F0 piano-roll + CQT + dF0/dt).

**BED:** BurstEpisodeDetector filters non-cry audio before reaching the classifier, maintaining FAR = 0.005 at the operating point.

---

## Evaluation

Evaluated using the **Polyphonic Sound Detection Score (PSDS)** — Bilen et al., ICASSP 2020. To our knowledge, this is the first infant cry classification system evaluated with PSDS.

| Metric | Value |
|--------|-------|
| **PSDS** | **0.8779** |
| F1 @ operating point | 0.956 |
| Precision | 0.995 |
| Recall | 0.920 |
| False Alarm Rate | 0.005 |
| Onset latency p50 | 0.0s |
| False positives (all classes) | **0** |

**Per-class recall @ threshold=0.10:**

| Class | Recall | FN | FP |
|-------|--------|----|----|
| pain | 0.960 | 2 | 0 |
| hunger | 0.900 | 5 | 0 |
| discomfort | 0.920 | 4 | 0 |
| tired | 0.900 | 5 | 0 |

**Evaluation protocol:** 200 synthetic streaming episodes (60s each), 18 thresholds swept, IOU criterion = 0.3, val_set_fixed_v3 (204 clips, zero train/val leakage).

The plateau between thresholds 0.10–0.35 with constant FAR=0.005 demonstrates robust threshold-independent behavior across the operating range.

Full results: [`evaluation/psds_summary.json`](evaluation/psds_summary.json)

---

## Dataset

Training data is drawn from four public sources:

| Source | License |
|--------|---------|
| DonateACry corpus | MIT |
| Dunstan Baby Language recordings | Research use |
| Kaggle BabyCry Sense | CC BY 4.0 |
| Mendeley 3-class segmented | CC BY 4.0 |

**Label auditing methodology:** Source labels from non-clinical crowdsourced datasets are challenged, not accepted at face value. We apply an acoustic criterion combining F0 profile, spectral centroid, and cross-model agreement to identify and exclude mislabeled clips. 91 low-pitch pain clips were excluded after analysis — criterion documented and reproducible.

**Train/validation separation:** The validation set is fixed (val_set_fixed_v3, 204 clips, zero augmentation). A train/validation leakage issue was identified and corrected: 86 Dunstan clips were removed from the validation set.

Preprocessing pipeline for DonateACry: [`data_prep/prep_donateacry.py`](data_prep/prep_donateacry.py)

---

## Repository contents

```
naps0-research/
├── README.md
├── index.html                   — project landing page (naps0.com)
├── data_prep/
│   └── prep_donateacry.py
└── evaluation/
    └── psds_summary.json
```

This repository contains research artifacts. Application code is proprietary.

---

## Citation

```
Naps0: Real-Time On-Device Infant Cry Classification with Hierarchical
Detection and PSDS Evaluation. Independent research, 2026.
Contact: research@naps0.com
```

---

## Contact

Research inquiries: **research@naps0.com**
Project website: **https://naps0.com**
