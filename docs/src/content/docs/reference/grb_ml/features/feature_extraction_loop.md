---
title: feature_extraction_loop
description: API Reference for grb_ml.features.feature_extraction_loop
---

**Module:** `grb_ml.features` | **Type:** `Function`



```python
def grb_ml.features.feature_extraction_loop(detector_counts, background_bins_number=100, foreground_bins_number=10)
```

Feature Extraction loop\

Args:\
    - `detector_counts` (type): output of simulations.detector_counts() \
    - `background_bins_number` (int): set to 100 by default \
    - `foreground_bins_number` (int): set to 10 by default \

Returns:\
    X (NumPy Array): of shape (n_valid_windows, 7), the feature matrix
