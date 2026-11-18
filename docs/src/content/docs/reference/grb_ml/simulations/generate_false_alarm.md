---
title: generate_false_alarm
description: Generates a short, sharp false alarm spike (e.g., cosmic ray hit).
---

<p class="api-meta"><span class="api-badge api-badge-function">function</span> <code>grb_ml.simulations</code></p>

```python
grb_ml.simulations.generate_false_alarm(duration_bins=2, amplitude=150)
```

Generates a short, sharp false alarm spike (e.g., cosmic ray hit).

Args:
    duration_bins (int): very short duration (1-2 bins)
    amplitude (int): peak count rate

Returns:
    Tuple of 2 NumPy Arrays (low and high channels)
