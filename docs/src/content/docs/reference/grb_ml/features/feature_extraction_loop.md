---
title: feature_extraction_loop
description: Extract the feature matrix by sliding over every valid bin.
---

<p class="api-meta"><span class="api-badge api-badge-function">function</span> <code>grb_ml.features</code></p>

```python
grb_ml.features.feature_extraction_loop(detector_counts, background_bins_number=100, foreground_bins_number=10)
```

Extract the feature matrix by sliding over every valid bin.

<p class="api-label">Parameters</p>

<dl class="api-params">
<dt><code>detector_counts</code> <span class="api-type">tuple of numpy.ndarray</span></dt>
<dd>

``(low_counts, high_counts)``.

</dd>
<dt><code>background_bins_number</code> <span class="api-type">int, default 100</span></dt>
<dd>

Background window size.

</dd>
<dt><code>foreground_bins_number</code> <span class="api-type">int, default 10</span></dt>
<dd>

Foreground window size.

</dd>
</dl>

<p class="api-label">Returns</p>

<dl class="api-params">
<dt><code>X</code> <span class="api-type">numpy.ndarray, shape (n_valid_windows, 7)</span></dt>
<dd>

Columns: SNR low, SNR high, HR, peak-to-mean low/high,
asymmetry low/high.

</dd>
</dl>

<p class="api-label">See Also</p>

- [`split_windows`](../split_windows/)
- [`compute_snr`](../compute_snr/)
- [`compute_hardness_ratio`](../compute_hardness_ratio/)
- [`compute_peak_to_mean_ratio`](../compute_peak_to_mean_ratio/)
- [`compute_asymmetry_ratio`](../compute_asymmetry_ratio/)
