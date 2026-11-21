---
title: grb_trigger.simulations
description: Overview of grb_trigger.simulations
sidebar:
  order: 0
---

This module is capable of generating synthetic singals of various
astronomical events detectable by GRB observing satellites. These include

- GRBs (gamma-ray bursts)
- background radiation
- false alarm (Dirac-delta alike peak, simulates cosmic-ray hit)
- SAA crossing (the South Atlantic Anomaly is a region in Low Earth Orbit
    (LEO) with more intrinsic natural radiation)

The `detector_counts()` function is capable of combining multiple
simulated events into a signal.

This module does not compute the features (tabular data that the model
can be trained with) or the actual arrays to be provided to the `scikit-learn`
model. See the `features.py` and `dataset.py` modules for that.

## Functions

| Function | Description |
| :--- | :--- |
| [`generate_background`](./generate_background/) | Generate Poisson background counts for both energy channels. |
| [`generate_grb_pulse`](./generate_grb_pulse/) | Generate a GRB pulse with a fast rise and exponential decay. |
| [`generate_false_alarm`](./generate_false_alarm/) | Generate a short, sharp spike mimicking a cosmic-ray hit. |
| [`generate_saa_crossing`](./generate_saa_crossing/) | Generate a slow, symmetric South Atlantic Anomaly crossing. |
| [`detector_counts`](./detector_counts/) | Inject events into a background time series. |
