#!/usr/bin/env python3
import numpy as np
from grb_ml.dataset import generate_labels

def test_generate_labels_grb_overlap():
    # 1. ARRANGE: Set up mock inputs
    n_bins = 20
    dummy_signal = (np.zeros(4), np.zeros(4))
    events = [
        {"signal": dummy_signal, "start_bin": 10, "type": "grb", "is_grb": 1}
    ]

    # 2. ACT: Run the function being tested
    y = generate_labels(
        n_bins=n_bins,
        events=events,
        background_bins_number=5,
        foreground_bins_number=4
        )

    # 3. ASSERT: Compare actual output against expected output
    expected_y = np.array([0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0])
    assert np.array_equal(y, expected_y)
