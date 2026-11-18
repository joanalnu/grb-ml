---
title: generate_labels
description: Produces the 1D target array matching the exact rows returned by features.feature_extraction_loop().
---

<p class="api-meta"><span class="api-badge api-badge-function">function</span> <code>grb_ml.dataset</code></p>

```python
grb_ml.dataset.generate_labels(n_bins, events, background_bins_number=100, foreground_bins_number=10)
```

Produces the 1D target array matching the exact rows returned by features.feature_extraction_loop().

<p class="api-label">Parameters</p>

<dl class="api-params">
<dt><code>n_bins</code> <span class="api-type">int</span></dt>
<dd>

signal length in bin number.

</dd>
<dt><code>events</code> <span class="api-type">list of dict</span></dt>
<dd>

Each dict has the keys ``"signal"`` (``(low, high)`` arrays),
``"start_bin"`` (int, > 0), ``"type"`` (str, e.g. ``"grb"``) and
optionally ``"is_grb"`` (0 or 1).

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
<dt><code>y</code> <span class="api-type">numpy.ndarray</span></dt>
<dd>

Target column: true if more than half of the window values are is_grb=1

</dd>
</dl>

<p class="api-label">Notes</p>

Returned array has shape (n,) with
`n = n_bins - background_bins_number - foreground_bins_number + 1`.
