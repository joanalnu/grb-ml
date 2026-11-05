---
title: generate_false_alarm
description: API Reference for grb_ml.simulations.generate_false_alarm
---

**Module:** `grb_ml.simulations` | **Type:** `Function`



```python
def grb_ml.simulations.generate_false_alarm(duration_bins=2, amplitude=150)
```

Generates a short, sharp false alarm spike (e.g., cosmic ray hit).

Args:
    duration_bins (int): very short duration (1-2 bins)
    amplitude (int): peak count rate

Returns:
    Tuple of 2 NumPy Arrays (low and high channels)
