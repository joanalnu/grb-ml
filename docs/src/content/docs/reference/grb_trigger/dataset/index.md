---
title: grb_trigger.dataset
description: Overview of grb_trigger.dataset
sidebar:
  order: 0
---

API reference for `grb_trigger.dataset`.

## Functions

| Function | Description |
| :--- | :--- |
| [`generate_labels`](./generate_labels/) | Produces the 1D target array matching the exact rows returned by features.feature_extraction_loop(). |
| [`generate_dataset`](./generate_dataset/) | Simulate n_orbits separate CubeSat orbits in a loop, where each orbit generates its own X_orbit and y_orbit with length `(n_bins - background_bins_number - foreground_bins_number + 1)`. |
