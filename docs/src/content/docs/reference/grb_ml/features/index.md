---
title: grb_ml.features
description: Overview of grb_ml.features
sidebar:
  order: 0
---

This module focuses on converting raw signals produced by `simulations.py`
into tabular data that can be used to train a `scikit-learn` model.

This module includes functions to compute different features and
wraps everything in the `feature_extraction_loop()` function which
returns the feature matrix (`numpy.ndarray` shape (n, 7), with `n`
propotional to `n_bins` of the signal.

The module that actually wraps the synthetic data generation and provides
the features and orbit dataframes is `dataset.py`. In this module, there
are functions available to compute the following features:

- SNR (signal-to-noise ratio)
- HR (hardness ratio)
- Peak to mean ration
- asummetry ratio

## Functions

| Function | Description |
| :--- | :--- |
| [`split_windows`](./split_windows/) | Split a detector time series into foreground and background windows. |
| [`compute_snr`](./compute_snr/) | Compute the signal-to-noise ratio of each energy channel. |
| [`compute_hardness_ratio`](./compute_hardness_ratio/) | Compute the hardness ratio (HR) of the background-subtracted signal. |
| [`compute_peak_to_mean_ratio`](./compute_peak_to_mean_ratio/) | Compute the peak-to-mean ratio of the foreground window. |
| [`compute_asymmetry_ratio`](./compute_asymmetry_ratio/) | Compute the temporal asymmetry of the foreground window. |
| [`feature_extraction_loop`](./feature_extraction_loop/) | Extract the feature matrix by sliding over every valid bin. |
