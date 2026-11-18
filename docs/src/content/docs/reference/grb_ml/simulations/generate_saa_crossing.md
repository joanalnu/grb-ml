---
title: generate_saa_crossing
description: Generates a slow, symmetric radiation belt crossing (e.g., South Atlantic Anomaly).
---

<p class="api-meta"><span class="api-badge api-badge-function">function</span> <code>grb_ml.simulations</code></p>

```python
grb_ml.simulations.generate_saa_crossing(duration_bins=300, amplitude=60, hardness_ratio=0.4)
```

Generates a slow, symmetric radiation belt crossing (e.g., South Atlantic Anomaly).

Args:
    duration_bins (int): duration of the crossing in bins
    amplitude (int): peak count rate in the low-energy channel
    hardness_ratio (float): ratio high_counts/low_counts (typically soft, < 1.0)

Returns:
    Tuple of 2 NumPy Arrays (low and high channels, each shape (duration_bins,))
