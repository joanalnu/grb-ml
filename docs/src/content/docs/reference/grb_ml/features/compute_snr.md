---
title: compute_snr
description: API Reference for grb_ml.features.compute_snr
---

**Module:** `grb_ml.features` | **Type:** `Function`



```python
def grb_ml.features.compute_snr(fg_window, bg_window)
```

Computes the signal-to-noise ratio (SNR) for a signal divided into foreground and background windows.

Args:
    fg_window (tuple of arrays): The foreground window returned by split_windows.
    bg_window (tuple of arrays): The background window returned by split_windows.

Returns:
    SNR (array of arrays): SNR for the low (index=0) and high (index=1) energy channels. The SNR is given by (mean_foreground - mean_background) / std_background, for each channel separately.
