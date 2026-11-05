---
title: compute_hardness_ratio
description: API Reference for grb_ml.features.compute_hardness_ratio
---

**Module:** `grb_ml.features` | **Type:** `Function`



```python
def grb_ml.features.compute_hardness_ratio(fg_window, bg_window)
```

Computes the hardness ratio (HR) for a detector signal splitted into background and foreground windows.

Args:
    fg_window (tuple of arrays): The foreground window returned by split_windows.
    bg_window (tuple of arrays): The background window returned by split_windows.

Returns:
    HR (int): hardness ratio for the signal given by (foreground_high_mean - background_high_mean) / (foreground_low_mean - background_low_mean)
