---
title: compute_snr
description: Compute the signal-to-noise ratio of each energy channel.
---

<p class="api-meta"><span class="api-badge api-badge-function">function</span> <code>grb_trigger.features</code></p>

```python
grb_trigger.features.compute_snr(fg_window, bg_window)
```

Compute the signal-to-noise ratio of each energy channel.

<p class="api-label">Parameters</p>

<dl class="api-params">
<dt><code>fg_window, bg_window</code> <span class="api-type">tuple of numpy.ndarray</span></dt>
<dd>

Windows returned by `split_windows`.

</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-params">
<dt><code>snr</code> <span class="api-type">numpy.ndarray, shape (2,)</span></dt>
<dd>

SNR of the low (index 0) and high (index 1) channel.

</dd>
</dl>

<p class="api-label">Raises</p>

<dl class="api-params">
<dt> <span class="api-type">ValueError</span></dt>
<dd>

If a window is empty or the background standard deviation is zero.

</dd>
</dl>

<p class="api-label">Notes</p>

For each channel,

$$\mathrm{SNR} = \frac{\bar{x}_\mathrm{fg} - \bar{x}_\mathrm{bg}}{\sigma_\mathrm{bg}}$$
