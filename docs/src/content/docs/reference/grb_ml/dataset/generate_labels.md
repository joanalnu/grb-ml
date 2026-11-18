---
title: generate_labels
description: Produces the 1D target array mathing the exact rows returned by features.feature_extraction_loop().\
---

<p class="api-meta"><span class="api-badge api-badge-function">function</span> <code>grb_ml.dataset</code></p>

```python
grb_ml.dataset.generate_labels(n_bins, events, background_bins_number=100, foreground_bins_number=10)
```

Produces the 1D target array mathing the exact rows returned by features.feature_extraction_loop().\

Args:\
    - n_bins (int): number of bins of ...\
    - events (list of dictionaries): with the structure events = [{"signal": (Array Tuple), "start_bin": (int), "type": (string; grb, cosmic_ray, or grb), "is_grb": (int; 0 or 1)}]\
    - background_bins_number (int): set to 100 by default\
    - foreground_bins_number (int): set to 10 by default\

Returns:
    - y (1D array): the target column (is_grb), if more than half of the bins are is_grb true
