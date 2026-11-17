---
title: generate_dataset
description: API Reference for grb_ml.dataset.generate_dataset
---

**Module:** `grb_ml.dataset` | **Type:** `Function`



```python
def grb_ml.dataset.generate_dataset(n_orbits=50, n_bins=1000)
```

Simulate n_orbits separate CubeSat orbits in a loop, where each orbit generates its own X_orbit and y_orbit with length (n_bins - background_bins_number - foreground_bins_number + 1).

Args:
    - n_orbits: ...
    - n_bins: ...

Returns:
    ...
