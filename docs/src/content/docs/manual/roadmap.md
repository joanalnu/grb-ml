---
title: "Project Roadmap"
author: joanalnu
description: "Details about future plans and steps to the completion of the GRB-ML package development."
---

> LLM assistance was used to help draft and polish this file.

# 🛰️ CubeSat GRB ML Trigger — Project Roadmap

## 📌 Project Overview
The goal of this project is to design, train, and package a lightweight Machine Learning trigger algorithm using `scikit-learn` capable of running onboard a Gamma-Ray Burst (GRB) CubeSat. The model must accurately distinguish rare astrophysical **Gamma-Ray Bursts (GRBs)** from **Poisson background noise**, **cosmic ray particle hits**, and **radiation belt crossings** (such as the South Atlantic Anomaly, or SAA) while respecting severe onboard compute and downlink constraints.

The project follows a dual-track workflow:
1. **Interactive Exploration:** Prototyping physics simulations, feature extraction, and ML classifiers in Jupyter Notebooks.
2. **Package Development:** Refactoring validated functions into a modular, well-tested, public Python package (`grb-trigger-ml`).

---

## 🗺️ Phase-by-Phase Development Plan

### Phase 1: Synthetic Data & Physics Simulation (`simulations.py`) — ✅ *Completed*
Build a realistic photon-counting time-series generator across two energy channels (**Low Energy:** $25	ext{--}100	ext{ keV}$, **High Energy:** $100	ext{--}300	ext{ keV}$).
- [x] **Poisson Background Generator (`generate_background`):** Simulate baseline sky noise.
- [x] **Real GRB Pulse Generator (`generate_grb_pulse`):** Model Fast Rise Exponential Decay (FRED) profiles with spectral hardness ($HR > 1.0$) and spectral cooling.
- [x] **Cosmic Ray Spike Generator (`generate_false_alarm`):** Simulate ultra-short ($1	ext{--}2$ bin) instrumental particle hits.
- [x] **Radiation Belt Crossing (`generate_saa_crossing`):** Model slow, smooth, spectrally soft ($HR < 1.0$) half-sine background swells.
- [x] **Multi-Event Timeline Injector (`detector_counts`):** Combine arbitrary dictionaries of events and ground-truth labels onto a baseline timeline.
- [x] **Visual Verification:** Plot dual-channel light curves with annotated event windows.

---

### Phase 2: Rolling-Window Feature Engineering (`features.py`) — 🔄 *Up Next*
Convert raw 1D photon count time series into a 2D tabular dataset suitable for `scikit-learn` classifiers.
- [ ] **Sliding Dual-Window Architecture:** Implement a rolling background window (e.g., $W_{	ext{bg}} = 100$ bins) and foreground trigger window (e.g., $W_{	ext{fg}} = 10$ bins) with a configurable buffer gap so rising GRB tails do not contaminate background estimates.
- [ ] **Multi-Timescale Signal-to-Noise Ratio (SNR):**
  $$	ext{SNR} = rac{\mu_{	ext{fg}} - \mu_{	ext{bg}}}{\sigma_{	ext{bg}}}$$
  Compute across short ($0.2	ext{ s}$), medium ($1.0	ext{ s}$), and long ($4.0	ext{ s}$) foreground windows.
- [ ] **Spectral Hardness Ratio ($HR$):** Calculate the ratio of background-subtracted high-energy counts to low-energy counts:
  $$HR = rac{\mu_{	ext{fg, high}} - \mu_{	ext{bg, high}}}{\mu_{	ext{fg, low}} - \mu_{	ext{bg, low}}}$$
- [ ] **Pulse Shape & Asymmetry Metrics:** Extract peak-to-mean ratio (to catch 1-bin cosmic rays) and rise-to-decay skewness within the foreground window.
- [ ] **Ground-Truth Labeling Pipeline:** Automatically label each rolling window (`1` = Real GRB active in foreground window, `0` = Background / SAA / Cosmic Ray).

---

### Phase 3: Dataset Generation & Exploratory Data Analysis (`dataset.py`)
Create a large, balanced/stratified benchmark dataset representing thousands of simulated CubeSat orbits.
- [ ] **Monte Carlo Orbit Generator:** Randomize GRB amplitudes, rise/decay constants ($	au_{	ext{rise}}, 	au_{	ext{decay}}$), hardness ratios, SAA durations, and cosmic ray frequencies.
- [ ] **Feature Separability Visualization:** Plot 2D scatter plots and corner plots (e.g., $	ext{SNR}_{	ext{short}}$ vs. $	ext{SNR}_{	ext{long}}$, $	ext{SNR}$ vs. $HR$) to visually inspect how classes separate.
- [ ] **Class Imbalance Strategy:** Configure realistic rarity ratios (e.g., $95\%$ noise/false alarms, $5\%$ real GRBs) and stratified train/validation/test splits (`StratifiedKFold`).

---

### Phase 4: Model Training & CubeSat Optimization (`models.py` & `evaluate.py`)
Train lightweight `scikit-learn` classifiers and evaluate them using mission-critical metrics.
- [ ] **Baseline Traditional Trigger:** Implement a classic $5\sigma$ SNR threshold trigger to serve as our scientific benchmark.
- [ ] **Supervised Tree Classifiers:** Train `RandomForestClassifier` and `HistGradientBoostingClassifier` with `class_weight="balanced"`.
- [ ] **Anomaly Detection Comparison:** Test `IsolationForest` to see if unsupervised learning can flag unseen transient types.
- [ ] **CubeSat Resource & Downlink Evaluation:**
  - Plot **Precision-Recall Curves** and compute **PR-AUC**.
  - Tune the probability trigger threshold (`predict_proba`) to maximize **Recall** (missed GRBs) under a strict **False Alarm Rate (FAR)** budget (e.g., $\le 1$ false alert per orbit).
  - Measure model memory footprint and single-window inference latency (targeting $< 5	ext{ ms}$).

---

### Phase 5: Real Space Telescope Validation (Optional Stretch Goal)
Test the trained pipeline on real archival gamma-ray burst data.
- [ ] **Fermi GBM / Swift BAT Ingestion:** Write a loader for public NASA FITS light-curve files.
- [ ] **Sim-to-Real Transfer Test:** Evaluate how well a model trained on synthetic FRED pulses generalizes to real cosmic bursts.

---

### Phase 6: Python Package Architecture & Release
Transition from prototype notebooks to an installable, open-source Python package.
```text
grb-trigger-ml/
├── pyproject.toml
├── README.md
├── LICENSE
├── src/
│   └── grb_trigger/
│       ├── __init__.py
│       ├── simulations.py   # Phase 1: Synthetic light curves
│       ├── features.py      # Phase 2: Rolling-window extractors
│       ├── dataset.py       # Phase 3: Batch simulation builder
│       ├── models.py        # Phase 4: Sklearn pipeline wrappers
│       └── evaluate.py      # Phase 4: PR curves & downlink metrics
├── notebooks/
│   ├── 01_signal_simulations.ipynb
│   ├── 02_feature_engineering.ipynb
│   └── 03_model_training_and_tuning.ipynb
└── tests/
    ├── test_simulations.py
    └── test_features.py
```
- [ ] **Unit Testing (`pytest`):** Write automated tests for edge cases, array shapes, and physical parameter bounds.
- [ ] **Documentation & Packaging:** Build package metadata with `pyproject.toml` and publish to GitHub / PyPI.

