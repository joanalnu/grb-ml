---
title: split_windows
description: Split a detector time series into foreground and background windows.
---

<p class="api-meta"><span class="api-badge api-badge-function">function</span> <code>grb_ml.features</code></p>

```python
grb_ml.features.split_windows(detector_counts, i, background_bins_number=100, foreground_bins_number=10)
```

Split a detector time series into foreground and background windows.

The background window holds the `background_bins_number` bins *before*
bin `i`; the foreground window holds the `foreground_bins_number` bins
starting *at* bin `i`.

<p class="api-label">Parameters</p>

<dl class="api-params">
<dt><code>detector_counts</code> <span class="api-type">tuple of numpy.ndarray</span></dt>
<dd>

``(low_counts, high_counts)``, as returned by
`simulations.detector_counts`.

</dd>
<dt><code>i</code> <span class="api-type">int</span></dt>
<dd>

Index of the first foreground bin.

</dd>
<dt><code>background_bins_number</code> <span class="api-type">int, default 100</span></dt>
<dd>

Number of bins in the background window.

</dd>
<dt><code>foreground_bins_number</code> <span class="api-type">int, default 10</span></dt>
<dd>

Number of bins in the foreground window.

</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-params">
<dt><code>fg_window</code> <span class="api-type">tuple of numpy.ndarray</span></dt>
<dd>

``(low, high)`` slices of the foreground window.

</dd>
<dt><code>bg_window</code> <span class="api-type">tuple of numpy.ndarray</span></dt>
<dd>

``(low, high)`` slices of the background window.

</dd>
</dl>

<p class="api-label">Raises</p>

<dl class="api-params">
<dt> <span class="api-type">ValueError</span></dt>
<dd>

If the channels are empty or differ in length, if a window size is
not positive, or if there are not enough bins around `i`.

</dd>
</dl>

<p class="api-label">See Also</p>

- [`feature_extraction_loop`](../feature_extraction_loop/) — Applies this function at every valid bin.

<p class="api-label">Examples</p>

```pycon
>>> bkg = generate_background(500)
>>> counts = detector_counts(bkg, [{"signal": generate_grb_pulse(50, 80),
...                                 "start_bin": 200, "type": "grb"}])
>>> fg, bg = split_windows(counts, 200)
>>> len(fg[0]), len(bg[0])
(10, 100)
```
