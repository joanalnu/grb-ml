---
title: detector_counts
description: API Reference for grb_ml.simulations.detector_counts (function)
---

```python
detector_counts(bkg, grb, start_bin=300)
```

Injects a GRB pulse into a background time series on the interval start_bin to start_bin+pulse_duration

Args:
    bkg (Array Tuple): Background counts Tuple of 2 NumPy Array (low and high channels)
    grb (Array Tuple): GRB pulse

Returns:
    Tuple of NumPy Arrays (same shape as bkg)