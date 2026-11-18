---
title: generate_false_alarm
description: Generate a short, sharp spike mimicking a cosmic-ray hit.
---

<p class="api-meta"><span class="api-badge api-badge-function">function</span> <code>grb_ml.simulations</code></p>

```python
grb_ml.simulations.generate_false_alarm(duration_bins=2, amplitude=150)
```

Generate a short, sharp spike mimicking a cosmic-ray hit.

<p class="api-label">Parameters</p>

<dl class="api-params">
<dt><code>duration_bins</code> <span class="api-type">int, default 2</span></dt>
<dd>

Duration of the spike in bins.

</dd>
<dt><code>amplitude</code> <span class="api-type">float, default 150</span></dt>
<dd>

Nominal peak count rate (randomly scaled by 0.8-1.2).

</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-params">
<dt><code>low, high</code> <span class="api-type">numpy.ndarray, shape (duration_bins,)</span></dt>
<dd>

Counts per channel; the high channel is ~1.1x the low channel.

</dd>
</dl>

<p class="api-label">Raises</p>

<dl class="api-params">
<dt> <span class="api-type">ValueError</span></dt>
<dd>

If `duration_bins` or `amplitude` is not positive.

</dd>
</dl>
