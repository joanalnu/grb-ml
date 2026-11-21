---
title: generate_grb_pulse
description: Generate a GRB pulse with a fast rise and exponential decay.
---

<p class="api-meta"><span class="api-badge api-badge-function">function</span> <code>grb_trigger.simulations</code></p>

```python
grb_trigger.simulations.generate_grb_pulse(duration_bins, amplitude, tau_rise=2.0, tau_decay=20.0, hardness_ratio=1.5)
```

Generate a GRB pulse with a fast rise and exponential decay.

<p class="api-label">Parameters</p>

<dl class="api-params">
<dt><code>duration_bins</code> <span class="api-type">int</span></dt>
<dd>

Duration of the pulse in bins.

</dd>
<dt><code>amplitude</code> <span class="api-type">float</span></dt>
<dd>

Peak count rate of the low channel.

</dd>
<dt><code>tau_rise</code> <span class="api-type">float, default 2.0</span></dt>
<dd>

Rise time constant.

</dd>
<dt><code>tau_decay</code> <span class="api-type">float, default 20.0</span></dt>
<dd>

Decay time constant (must be >= `tau_rise`).

</dd>
<dt><code>hardness_ratio</code> <span class="api-type">float, default 1.5</span></dt>
<dd>

High/low channel rate ratio, in [1.0, 2.5].

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

The low-channel rate is

$$r(t) = A\,(1 - e^{-t/\tau_r})\,e^{-t/\tau_d}$$

and the high channel is ``hardness_ratio * r(t)``.
