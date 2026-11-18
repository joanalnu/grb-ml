---
title: generate_background
description: Generate Poisson background counts for both energy channels.
---

<p class="api-meta"><span class="api-badge api-badge-function">function</span> <code>grb_ml.simulations</code></p>

```python
grb_ml.simulations.generate_background(n_bins, lam_low=40, lam_high=15)
```

Generate Poisson background counts for both energy channels.

<p class="api-label">Parameters</p>

<dl class="api-params">
<dt><code>n_bins</code> <span class="api-type">int</span></dt>
<dd>

Number of time bins.

</dd>
<dt><code>lam_low</code> <span class="api-type">float, default 40</span></dt>
<dd>

Mean count per bin, low-energy channel.

</dd>
<dt><code>lam_high</code> <span class="api-type">float, default 15</span></dt>
<dd>

Mean count per bin, high-energy channel.

</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-params">
<dt><code>low, high</code> <span class="api-type">numpy.ndarray, shape (n_bins,)</span></dt>
<dd>

Background counts per channel.

</dd>
</dl>

<p class="api-label">Raises</p>

<dl class="api-params">
<dt> <span class="api-type">ValueError</span></dt>
<dd>

If a rate is negative.

</dd>
</dl>

<p class="api-label">Examples</p>

```pycon
>>> low, high = generate_background(1000)
>>> low.shape
(1000,)
```
