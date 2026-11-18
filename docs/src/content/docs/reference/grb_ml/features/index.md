---
title: grb_ml.features
description: Overview of grb_ml.features
sidebar:
  order: 0
---

This is an introduction tot he features module.

I hope this texts pop-up in the index page for the module in the documentation.

## Functions

| Function | Description |
| :--- | :--- |
| [`split_windows`](./split_windows/) | Split a detector time series into foreground and background windows. |
| [`compute_snr`](./compute_snr/) | Compute the signal-to-noise ratio of each energy channel. |
| [`compute_hardness_ratio`](./compute_hardness_ratio/) | Compute the hardness ratio (HR) of the background-subtracted signal. |
| [`compute_peak_to_mean_ratio`](./compute_peak_to_mean_ratio/) | Compute the peak-to-mean ratio of the foreground window. |
| [`compute_asymmetry_ratio`](./compute_asymmetry_ratio/) | Compute the temporal asymmetry of the foreground window. |
| [`feature_extraction_loop`](./feature_extraction_loop/) | Extract the feature matrix by sliding over every valid bin. |
