---
title: compute_hardness_ratio
description: Compute the hardness ratio (HR) of the background-subtracted signal.
---

<p class="api-meta"><span class="api-badge api-badge-function">function</span> <code>grb_trigger.features</code></p>

```python
grb_trigger.features.compute_hardness_ratio(fg_window, bg_window)
```

Compute the hardness ratio (HR) of the background-subtracted signal.

<p class="api-label">Parameters</p>

<dl class="api-params">
<dt><code>fg_window, bg_window</code> <span class="api-type">tuple of numpy.ndarray</span></dt>
<dd>

Windows returned by `split_windows`.

</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-params">
<dt> <span class="api-type">float</span></dt>
<dd>

Net high-channel rate divided by net low-channel rate. ``0.0`` if
either net rate is not positive.

</dd>
</dl>

<p class="api-label">Raises</p>

<dl class="api-params">
<dt> <span class="api-type">ValueError</span></dt>
<dd>

If a window is empty.

</dd>
</dl>

<p class="api-label">Notes</p>

$$\mathrm{HR} = \frac{\bar{x}^\mathrm{high}_\mathrm{fg} - \bar{x}^\mathrm{high}_\mathrm{bg}}{\bar{x}^\mathrm{low}_\mathrm{fg} - \bar{x}^\mathrm{low}_\mathrm{bg}}$$
