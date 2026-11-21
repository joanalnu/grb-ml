---
title: compute_peak_to_mean_ratio
description: Compute the peak-to-mean ratio of the foreground window.
---

<p class="api-meta"><span class="api-badge api-badge-function">function</span> <code>grb_trigger.features</code></p>

```python
grb_trigger.features.compute_peak_to_mean_ratio(fg_window)
```

Compute the peak-to-mean ratio of the foreground window.

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

``max / mean`` for the low and high channel (``0`` if the mean is 0).

</dd>
</dl>

<p class="api-label">Raises</p>

<dl class="api-params">
<dt> <span class="api-type">ValueError</span></dt>
<dd>

If a channel of `fg_window` is empty.

</dd>
</dl>
