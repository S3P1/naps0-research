# Naps0 — On-Device Infant Cry Classification

> Real-time, privacy-first baby cry monitor for Android.  
> Classifies infant crying into four categories — **pain · hunger · discomfort · tired** — entirely on-device, with no cloud, no data upload, and no subscription.

---

## What it does

Naps0 listens continuously to a baby's cry and classifies the underlying need in real time. The entire inference pipeline runs on the Android device — no audio is ever transmitted to any server.

**Input:** continuous microphone stream (16 kHz)  
**Output:** differentiated push notification per class, with onset latency under 100ms

---

## Key Results

| Metric | Value |
|--------|-------|
| **PSDS** (primary metric) | **0.9424** |
| F1 @ operating threshold | 0.935 |
| False Alarm Rate | 0.065 |
| Pain recall (streaming) | 0.960 |
| Hunger recall | 0.900 |
| Discomfort recall | 0.940 |
| Tired recall | 0.940 |
| False Positives (all classes, operating zone) | **0** |
| Onset latency p50 / p90 | 0.0s / 0.051s |

Full results: [`evaluation/psds_summary.json`](evaluation/psds_summary.json)

---

## Evaluation Methodology

This is the central methodological contribution of the project.

Standard accuracy metrics in infant cry classification are systematically inflated by two problems:

**1. Data leakage.** Most published systems assign clips randomly to train/test sets without separating by infant identity. The model learns to recognise the individual infant's voice, not the cry category. Studies that apply leave-one-subject-out evaluation report 5–15 point accuracy drops compared to random splits (Nakano et al., 2019; Ji et al., 2021).

**2. Threshold dependence.** Reporting a single F1 score at a fixed threshold conceals the system's behavior across its full operating range — a critical flaw for real-time monitoring systems where the operating point is application-dependent.

Naps0 addresses both using **Polyphonic Sound Detection Score (PSDS)**, the evaluation standard from the DCASE sound event detection community (Bilen et al., ICASSP 2020):

- Evaluated over **200 synthetic streaming episodes** — not pre-segmented clips
- Across **18 decision thresholds** (0.10 → 0.55)
- Using **intersection-based TP/FP decisions** (IOU = 0.3) — robust to annotation boundary subjectivity
- With **cross-trigger penalty** — confusion between classes is penalised as a false positive
- **PSDS = area under the PSD-ROC curve** — threshold-independent, single comparable number

To our knowledge, this is the first infant cry classification system evaluated with PSDS.

---

## Dataset

Training set built from four public sources with scientific label auditing:

| Class | Original clips | Augmented | Total |
|-------|---------------|-----------|-------|
| pain | 388 | 421 | 809 |
| hunger | 911 | 308 | 1,219 |
| discomfort | 933 | 0 | 933 |
| tired | 155 | 242 | 397 |
| **Total** | **2,387** | **971** | **3,358** |

**Sources:** DonateACry · Dunstan Baby Language · Kaggle BabyCry Sense · Mendeley 3-class

**Validation set:** 250 clips, originals only, fixed split (`val_set_fixed_v2.csv`). No augmented data in validation.

### Label auditing methodology

Each source label was validated against acoustic criteria before inclusion in training. Non-clinical crowdsourced datasets contain a non-trivial proportion of mislabeled clips that inflate reported metrics when used without auditing.

Our auditing criterion combines three signals:
- Fundamental frequency (F0) profile relative to class distribution
- Spectral centroid consistency with the assigned class
- Cross-model agreement between independent classifiers

Applying this criterion, **91 pain clips were excluded** after cross-model analysis identified probable source mislabeling (median F0 = 244 Hz vs. 435 Hz for clean pain clips; 91% assigned to *hunger* by an independent classifier). The exclusion criterion is documented and reproducible.

This auditing methodology is a transferable contribution: a principled, acoustic-evidence-based approach to challenging non-clinical labels in publicly available datasets.

---

## Repository Structure

```
naps0-research/
├── README.md
├── data_prep/
│   └── prep_donateacry.py     ← DonateACry preprocessing pipeline
├── evaluation/
│   └── psds_summary.json      ← Full PSDS results (reproducible)
├── paper/
│   └── naps0_preprint.pdf     ← Preprint (when published)
└── results/
    └── psd_roc_curve.csv      ← PSD-ROC curve data
```

---

## Paper

Manuscript in preparation.  
Target venue: **DCASE Workshop 2026** / **Interspeech 2027**

Topics:
- PSDS evaluation protocol applied to infant cry classification
- Scientific label auditing methodology for non-clinical crowdsourced datasets
- On-device deployment constraints and design decisions
- Real-world out-of-distribution validation

---

## App

The Naps0 Android app is under private development.  
Website: [naps0.com](https://naps0.com)  
Research contact: research@naps0.com

---

## References

- Bilen, Ç. et al. (2020). *A Framework for the Robust Evaluation of Sound Event Detection.* ICASSP 2020.
- Ebbers, J. et al. (2022). *Threshold Independent Evaluation of Sound Event Detection Scores.* ICASSP 2022.
- Ferretti, G. et al. (2020). *DonateACry corpus.* Data in Brief, 29.
- Ji, C. et al. (2021). *Infant cry classification using Transformer-based model.* IEEE Access, 9.
- Nakano, H. et al. (2019). *Infant cry classification using CNN-LSTM.* ICASSP 2019.

---

## License

Research code in this repository: **MIT License**  
The Naps0 app and trained models are proprietary.  
Dataset licenses: DonateACry (MIT) · Mendeley (CC-BY)
