---
title: grb_ml.simulations
description: Overview of grb_ml.simulations
sidebar:
  order: 0
---

API reference for `grb_ml.simulations`.

## Functions

| Function | Description |
| :--- | :--- |
| [`detector_counts`](./detector_counts/) | Injects events (GRB pulse, cosmic ray, SSA, ...) into a background time series on the interval start_bin to start_bin+event_duration for n events. |
| [`generate_background`](./generate_background/) | Generates background radiation noise with Poisson distribution. |
| [`generate_false_alarm`](./generate_false_alarm/) | Generates a short, sharp false alarm spike (e.g., cosmic ray hit). |
| [`generate_grb_pulse`](./generate_grb_pulse/) | Generates the photon count rate of a GRB signal. |
| [`generate_saa_crossing`](./generate_saa_crossing/) | Generates a slow, symmetric radiation belt crossing (e.g., South Atlantic Anomaly). |
