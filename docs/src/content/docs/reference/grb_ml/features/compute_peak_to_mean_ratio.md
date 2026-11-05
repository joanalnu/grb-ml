---
title: compute_peak_to_mean_ratio
description: API Reference for grb_ml.features.compute_peak_to_mean_ratio
---

**Module:** `grb_ml.features` | **Type:** `Function`



```python
def grb_ml.features.compute_peak_to_mean_ratio(fg_window)
```

...

Args:
    fg_window (tuple of arrays): The foreground window returned by split_windows.

Returns:
    Array of values containing the peak-to-mean ratio for the low-energy (index=0) and high-energy (index=1) channels.
