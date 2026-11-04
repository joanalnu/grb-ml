---
title: generate_background
description: API Reference for grb_ml.simulations.generate_background (function)
---

```python
generate_background(n_bins, lam_low=40, lam_high=15)
```

Generates background radiation noise with Poisson distribution.

Args:
    n_bins (int): number of times bins with lam_low+lam_high counts each
    lam_low (int): average rate of the low-energy channel
    lam_high (int): average rate of the high-energy channel

Returns:
    Tuple of 2 NumPy Arrays (each shape (n_bins,))