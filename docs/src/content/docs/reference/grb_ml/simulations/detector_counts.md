---
title: detector_counts
description: Inject events into a background time series.
---

<p class="api-meta"><span class="api-badge api-badge-function">function</span> <code>grb_ml.simulations</code></p>

```python
grb_ml.simulations.detector_counts(bkg, events)
```

Inject events into a background time series.

<p class="api-label">Parameters</p>

<dl class="api-params">
<dt><code>bkg</code> <span class="api-type">tuple of numpy.ndarray</span></dt>
<dd>

``(low, high)`` background counts.

</dd>
<dt><code>events</code> <span class="api-type">list of dict</span></dt>
<dd>

Each dict has the keys ``"signal"`` (``(low, high)`` arrays),
``"start_bin"`` (int, > 0), ``"type"`` (str, e.g. ``"grb"``) and
optionally ``"is_grb"`` (0 or 1).

</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-params">
<dt><code>low, high</code> <span class="api-type">numpy.ndarray</span></dt>
<dd>

Copies of the background with all events added.

</dd>
</dl>

<p class="api-label">Raises</p>

<dl class="api-params">
<dt> <span class="api-type">ValueError</span></dt>
<dd>

If `events` is empty, channel lengths differ, an event does not fit
in the background, or ``start_bin`` is not positive.

</dd>
</dl>

<p class="api-label">See Also</p>

- [`generate_background`](../generate_background/)
- [`generate_grb_pulse`](../generate_grb_pulse/)
