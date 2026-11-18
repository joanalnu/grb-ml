import numpy as np

def split_windows(detector_counts, i, background_bins_number=100, foreground_bins_number=10):
    """
    Split a detector time series into foreground and background windows.

    The background window holds the `background_bins_number` bins *before*
    bin `i`; the foreground window holds the `foreground_bins_number` bins
    starting *at* bin `i`.

    Parameters
    ----------
    detector_counts : tuple of numpy.ndarray
        ``(low_counts, high_counts)``, as returned by
        `simulations.detector_counts`.
    i : int
        Index of the first foreground bin.
    background_bins_number : int, default 100
        Number of bins in the background window.
    foreground_bins_number : int, default 10
        Number of bins in the foreground window.

    Returns
    -------
    fg_window : tuple of numpy.ndarray
        ``(low, high)`` slices of the foreground window.
    bg_window : tuple of numpy.ndarray
        ``(low, high)`` slices of the background window.

    Raises
    ------
    ValueError
        If the channels are empty or differ in length, if a window size is
        not positive, or if there are not enough bins around `i`.

    See Also
    --------
    feature_extraction_loop : Applies this function at every valid bin.

    Examples
    --------
    >>> bkg = generate_background(500)
    >>> counts = detector_counts(bkg, [{"signal": generate_grb_pulse(50, 80),
    ...                                 "start_bin": 200, "type": "grb"}])
    >>> fg, bg = split_windows(counts, 200)
    >>> len(fg[0]), len(bg[0])
    (10, 100)
    """

    low_counts, high_counts = detector_counts
    if len(low_counts)<=0:
        raise ValueError("Low-energy channel detector counts must have positive length.")
    if len(high_counts)<=0:
        raise ValueError("High-energy channel detector counts must have positive length.")

    if len(low_counts)!=len(high_counts):
        raise ValueError(f"Length of high-energy and low-energy channel detector counts arrays must be equal: low_counts={len(low_counts)} and high_counts={len(high_counts)}.")

    if background_bins_number<=0:
        raise ValueError("background_bins_number must be positive.")
    if foreground_bins_number<=0:
        raise ValueError("foreground_bins_number must be positive.")

    if i<background_bins_number:
        raise ValueError(f"There are no enough background bins before bin {i} for background_bins_number={background_bins_number}.")
    if len(low_counts)-i<foreground_bins_number:
        raise ValueError(f"There are no enough foreground bins after bin {i} for foreground_bins_number={foreground_bins_number}.")

    bg_low = low_counts[i-background_bins_number:i]
    bg_high = high_counts[i-background_bins_number:i]
    bg_window = (bg_low, bg_high)

    fg_low = low_counts[i:i+foreground_bins_number]
    fg_high = high_counts[i:i+foreground_bins_number]
    fg_window = (fg_low, fg_high)


    return (fg_window, bg_window)


def compute_snr(fg_window, bg_window):
    """
    Compute the signal-to-noise ratio of each energy channel.

    Parameters
    ----------
    fg_window, bg_window : tuple of numpy.ndarray
        Windows returned by `split_windows`.

    Returns
    -------
    snr : numpy.ndarray, shape (2,)
        SNR of the low (index 0) and high (index 1) channel.

    Raises
    ------
    ValueError
        If a window is empty or the background standard deviation is zero.

    Notes
    -----
    For each channel,

    .. math:: \\mathrm{SNR} = \\frac{\\bar{x}_\\mathrm{fg} - \\bar{x}_\\mathrm{bg}}{\\sigma_\\mathrm{bg}}
    """
    snr = np.zeros(2)

    # lows come first with index 0, highs come second with index 1
    for i in range(2): # stops before 2, so at 1
        if len(fg_window[i]) == 0 or len(bg_window[i]) == 0:
            raise ValueError(f"Window for channel {i} cannot be empty.")

        bg_std = np.std(bg_window[i])
        if bg_std==0:
            raise ValueError("Standard devitation of background signal is 0.")
        snr[i] = (np.mean(fg_window[i]) - np.mean(bg_window[i])) / bg_std

    return snr


def compute_hardness_ratio(fg_window, bg_window):
    """
    Compute the hardness ratio (HR) of the background-subtracted signal.

    Parameters
    ----------
    fg_window, bg_window : tuple of numpy.ndarray
        Windows returned by `split_windows`.

    Returns
    -------
    float
        Net high-channel rate divided by net low-channel rate. ``0.0`` if
        either net rate is not positive.

    Raises
    ------
    ValueError
        If a window is empty.

    Notes
    -----
    .. math:: \\mathrm{HR} = \\frac{\\bar{x}^\\mathrm{high}_\\mathrm{fg} - \\bar{x}^\\mathrm{high}_\\mathrm{bg}}{\\bar{x}^\\mathrm{low}_\\mathrm{fg} - \\bar{x}^\\mathrm{low}_\\mathrm{bg}}
    """

    for i in range(2):
        if len(fg_window[i]) == 0 or len(bg_window[i]) == 0:
            raise ValueError(f"Window for channel {i} cannot be empty.")

    net_low = np.mean(fg_window[0]) - np.mean(bg_window[0])
    net_high = np.mean(fg_window[1]) - np.mean(bg_window[1])

    if net_low <= 0 or net_high <= 0:
        return 0.0

    return float(net_high / net_low)


def compute_peak_to_mean_ratio(fg_window):
    """
    Compute the peak-to-mean ratio of the foreground window.

    Parameters
    ----------
    fg_window : tuple of numpy.ndarray
        Foreground window returned by `split_windows`.

    Returns
    -------
    numpy.ndarray, shape (2,)
        ``max / mean`` for the low and high channel (``0`` if the mean is 0).

    Raises
    ------
    ValueError
        If a channel of `fg_window` is empty.
    """

    peak2mean_ratio = np.zeros(2)

    for i in range(2):

        if len(fg_window[i])==0:
            raise ValueError(f"Array of channel {i} in fg_window must not be empty.")

        fg_mean = np.mean(fg_window[i])

        if fg_mean==0:
            peak2mean_ratio[i] = 0
        else:
            peak2mean_ratio[i] = np.max(fg_window[i]) / fg_mean

    return peak2mean_ratio


def compute_asymmetry_ratio(fg_window):
    """
    Compute the temporal asymmetry of the foreground window.

    Parameters
    ----------
    fg_window : tuple of numpy.ndarray
        Foreground window returned by `split_windows`.

    Returns
    -------
    numpy.ndarray, shape (2,)
        Mean of the first half divided by mean of the second half, for the
        low and high channel (``0`` if the second-half mean is 0).

    Raises
    ------
    ValueError
        If a channel has two or fewer bins.

    Notes
    -----
    GRB pulses rise fast and decay slowly, so they give values above 1;
    symmetric events (e.g. SAA crossings) give values near 1.
    """

    asymmetry_ratio = np.zeros(2)

    for i in range(2):
        
        if len(fg_window[i])<=2:
            raise ValueError(f"Array length for channel {i} must be greater than 2 to compute the asymmetry ratio.")

        mid = len(fg_window[i]) // 2

        first_mean = np.mean(fg_window[i][:mid])
        second_mean = np.mean(fg_window[i][mid:])

        if second_mean==0:
            asymmetry_ratio[i]=0

        else:
            asymmetry_ratio[i] = first_mean/second_mean

    return asymmetry_ratio


def feature_extraction_loop(detector_counts, background_bins_number=100, foreground_bins_number=10):
    """
    Extract the feature matrix by sliding over every valid bin.

    Parameters
    ----------
    detector_counts : tuple of numpy.ndarray
        ``(low_counts, high_counts)``.
    background_bins_number : int, default 100
        Background window size.
    foreground_bins_number : int, default 10
        Foreground window size.

    Returns
    -------
    X : numpy.ndarray, shape (n_valid_windows, 7)
        Columns: SNR low, SNR high, HR, peak-to-mean low/high,
        asymmetry low/high.

    See Also
    --------
    split_windows
    compute_snr
    compute_hardness_ratio
    compute_peak_to_mean_ratio
    compute_asymmetry_ratio
    """

    X = []

    l = len(detector_counts[0])
    for i in range(background_bins_number, l-foreground_bins_number +1):
        fg_window, bg_window = split_windows(detector_counts, i, background_bins_number, foreground_bins_number)

        snr = compute_snr(fg_window, bg_window)
        hr = compute_hardness_ratio(fg_window, bg_window)
        p2m = compute_peak_to_mean_ratio(fg_window)
        asym = compute_asymmetry_ratio(fg_window)

        # np.concatenate automatically handles the fact that hr is 1dim while the rest are 2dim tuples
        new_entry = np.concatenate([snr, [hr], p2m, asym])
        X.append(new_entry)

    X = np.array(X)

    return X
