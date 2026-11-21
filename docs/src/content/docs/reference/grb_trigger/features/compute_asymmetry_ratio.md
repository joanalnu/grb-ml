---
title: compute_asymmetry_ratio
description: Compute the temporal asymmetry of the foreground window.
---

<p class="api-meta"><span class="api-badge api-badge-function">function</span> <code>grb_trigger.features</code></p>

```python
grb_trigger.features.compute_asymmetry_ratio(fg_window)
```

Compute the temporal asymmetry of the foreground window.

<p class="api-label">Parameters</p>

<dl class="api-params">
<dt><code>fg_window</code> <span class="api-type">tuple of numpy.ndarray</span></dt>
<dd>

Foreground window returned by `split_windows`.

</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-params">
<dt> <span class="api-type">numpy.ndarray, shape (2,)</span></dt>
<dd>

Mean of the first half divided by mean of the second half, for the
low and high channel (``0`` if the second-half mean is 0).

</dd>
</dl>

<p class="api-label">Raises</p>

<dl class="api-params">
<dt> <span class="api-type">ValueError</span></dt>
<dd>

If a channel has two or fewer bins.

</dd>
</dl>

<p class="api-label">Notes</p>

GRB pulses rise fast and decay slowly, so they give values above 1;
symmetric events (e.g. SAA crossings) give values near 1.
