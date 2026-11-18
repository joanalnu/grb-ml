---
title: generate_dataset
description: Simulate n_orbits separate CubeSat orbits in a loop, where each orbit generates its own X_orbit and y_orbit with length `(n_bins - background_bins_number - foreground_bins_number + 1)`.
---

<p class="api-meta"><span class="api-badge api-badge-function">function</span> <code>grb_ml.dataset</code></p>

```python
grb_ml.dataset.generate_dataset(n_orbits=50, n_bins=1000)
```

Simulate n_orbits separate CubeSat orbits in a loop, where each orbit generates its own X_orbit and y_orbit with length `(n_bins - background_bins_number - foreground_bins_number + 1)`.

<p class="api-label">Parameters</p>

<dl class="api-params">
<dt><code>n_orbits</code> <span class="api-type">int, default 50</span></dt>
<dd>

Number of separate orbits to simulate.

</dd>
<dt><code>n_bins</code> <span class="api-type">int, default 1000</span></dt>
<dd>

Number of bins in an orbit, each bin is a photon count recording.

</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-params">
<dt><code>X_orbit</code> <span class="api-type">numpy.ndarray (n, 7)</span></dt>
<dd>

The feature matrix compiled with the results of the
simulation module

</dd>
<dt><code>y_orbit</code> <span class="api-type">numpy.ndarray (n, )</span></dt>
<dd>

The target array with the information returned by generate_labels

</dd>
</dl>

<p class="api-label">Notes</p>

Each orbit has a signal with length n_bins.

The length each orbit signal after applying the background
and foreground cuts (length of the output) `n = n_bins -
background_bins_number - foreground_bins_number + 1`.
