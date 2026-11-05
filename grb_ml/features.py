import numpy as np

def split_windows(detector_counts, i, background_bins_number=100, foreground_bins_number=10):
    """
    Splits the detected signal counts into a background window (100 bins before given bin i) and a foreground window (10 bins after i).\\

    Args:\\
        - `detector_counts` (type): output of simulations.detector_counts() \\
        - `i`: the bin index to split \\
        - `background_bins_number` (int): set to 100 by default \\
        - `foreground_bins_number` (int): set to 10 by default \\

    Returns:\\
        - Tuple of Tuples of arrays. Returns `(fg_window, bg_window)` each being a tuple of array containing the low-energy and high-energy channels slices of the original array for the foreground and background window respectively.
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
    Computes the signal-to-noise ratio (SNR) for a signal divided into foreground and background windows.

    Args:
        fg_window (tuple of arrays): The foreground window returned by split_windows.
        bg_window (tuple of arrays): The background window returned by split_windows.

    Returns:
        SNR (array of arrays): SNR for the low (index=0) and high (index=1) energy channels. The SNR is given by (mean_foreground - mean_background) / std_background, for each channel separately.

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
    Computes the hardness ratio (HR) for a detector signal splitted into background and foreground windows.

    Args:
        fg_window (tuple of arrays): The foreground window returned by split_windows.
        bg_window (tuple of arrays): The background window returned by split_windows.

    Returns:
        HR (int): hardness ratio for the signal given by (foreground_high_mean - background_high_mean) / (foreground_low_mean - background_low_mean)
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
    ...

    Args:
        fg_window (tuple of arrays): The foreground window returned by split_windows.

    Returns:
        Array of values containing the peak-to-mean ratio for the low-energy (index=0) and high-energy (index=1) channels.

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
    ...

    Args:
        fg_window (tuple of arrays): The foreground window returned by split_windows.
        
    Returns:
        ...
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


def feature_extraction_loop():
    """
    Feature Extraction loop

    Args:
        ...

    Returns:
        ...
    """

    return None
