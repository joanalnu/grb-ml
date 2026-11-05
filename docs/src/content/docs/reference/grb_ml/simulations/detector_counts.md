---
title: detector_counts
description: API Reference for grb_ml.simulations.detector_counts
---

**Module:** `grb_ml.simulations` | **Type:** `Function`



```python
def grb_ml.simulations.detector_counts(bkg, events)
```

Injects events (GRB pulse, cosmic ray, SSA, ...) into a background time series on the interval start_bin to start_bin+event_duration for n events.

Args:
    bkg (Array Tuple): Background coutns Tuple of 2 NumPy Array (low and high channels)
    events (List of Dictionaries): With the structure:
    events = [
        {"signal": (Array Tuple), "start_bin": (int), "type": (string; grb, cosmic_ray, or grb), "is_grb": (int; 0 or 1)}
    ]

Returns:
    Tuple of 2 Arrays with the size of the background input with the injected events.
