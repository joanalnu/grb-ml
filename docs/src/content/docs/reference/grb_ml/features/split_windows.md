---
title: split_windows
description: API Reference for grb_ml.features.split_windows
---

**Module:** `grb_ml.features` | **Type:** `Function`



```python
def grb_ml.features.split_windows(detector_counts, i, background_bins_number=100, foreground_bins_number=10)
```

Splits the detected signal counts into a background window (100 bins before given bin i) and a foreground window (10 bins after i).\

Args:\
    - `detector_counts` (type): output of simulations.detector_counts() \
    - `i`: the bin index to split \
    - `background_bins_number` (int): set to 100 by default \
    - `foreground_bins_number` (int): set to 10 by default \

Returns:\
    - Tuple of Tuples of arrays. Returns `(fg_window, bg_window)` each being a tuple of array containing the low-energy and high-energy channels slices of the original array for the foreground and background window respectively.
