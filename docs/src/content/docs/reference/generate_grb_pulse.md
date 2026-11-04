---
title: generate_grb_pulse
description: API Reference for grb_ml.simulations.generate_grb_pulse (function)
---

```python
generate_grb_pulse(duration_bins, amplitude, tau_rise=2.0, tau_decay=20.0, hardness_ratio=1.5)
```

Generates the photon count rate of a GRB signal.

Args:
    duration_bins (int) duration of the signal
    amplitude (int): peak count rate
    tau_rise (float): rise time constant
    tau_decay (float): decay time constant
    hardness_ratio (float): ratio high_counts/low_counts

Returns:
    Tuple of 2 NumPy Arrays (each shape (duration_bins,))