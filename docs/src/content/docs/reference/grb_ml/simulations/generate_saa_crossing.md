---
title: generate_saa_crossing
description: Generate a slow, symmetric South Atlantic Anomaly crossing.
---

<p class="api-meta"><span class="api-badge api-badge-function">function</span> <code>grb_ml.simulations</code></p>

```python
grb_ml.simulations.generate_saa_crossing(duration_bins=300, amplitude=60, hardness_ratio=0.4)
```

Generate a slow, symmetric South Atlantic Anomaly crossing.

<p class="api-label">Parameters</p>

<dl class="api-params">
<dt><code>duration_bins</code> <span class="api-type">int, default 300</span></dt>
<dd>

Duration of the crossing in bins.

</dd>
<dt><code>amplitude</code> <span class="api-type">float, default 60</span></dt>
<dd>

Peak low-channel count rate.

</dd>
<dt><code>hardness_ratio</code> <span class="api-type">float, default 0.4</span></dt>
<dd>

High/low channel ratio, in (0, 1] (a soft spectrum).

</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-params">
<dt><code>low, high</code> <span class="api-type">numpy.ndarray, shape (duration_bins,)</span></dt>
<dd>

Poisson-sampled counts per channel.

</dd>
</dl>

<p class="api-label">Raises</p>

<dl class="api-params">
<dt> <span class="api-type">ValueError</span></dt>
<dd>

If an argument is outside its allowed range.

</dd>
</dl>

<p class="api-label">Notes</p>

The rate follows a half sine wave, $A\sin(\pi t / T)$.
