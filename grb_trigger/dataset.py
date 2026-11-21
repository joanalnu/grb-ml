import numpy as np

def generate_labels(n_bins, events, background_bins_number=100, foreground_bins_number=10):
    """
    Produces the 1D target array matching the exact rows returned by features.feature_extraction_loop().

    Parameters
    ----------
    n_bins : int
        signal length in bin number.
    events : list of dict
        Each dict has the keys ``"signal"`` (``(low, high)`` arrays),
        ``"start_bin"`` (int, > 0), ``"type"`` (str, e.g. ``"grb"``) and
        optionally ``"is_grb"`` (0 or 1).
    background_bins_number : int, default 100
        Number of bins in the background window.
    foreground_bins_number : int, default 10
        Number of bins in the foreground window.

    Returns
    -------
    y : numpy.ndarray
        Target column: true if more than half of the window values are is_grb=1

    Notes
    -----
    Returned array has shape (n,) with
    `n = n_bins - background_bins_number - foreground_bins_number + 1`.

    """

    # 1. Create a blank 1D mask of 0s (length = total bins in the orbit)
    grb_mask = np.zeros(n_bins, dtype=int)

    # 2. Mark the exact bins where a real GRB ("is_grb" == 1) is active
    for event in events:
        if event["is_grb"] == 1:
            start = event["start_bin"]
            duration = len(event["signal"][0])
            grb_mask[start : start + duration] = 1

    # 3. Slide across the exact same valid indices as feature_extraction_loop
    y = []
    for i in range(background_bins_number, n_bins - foreground_bins_number + 1):
        # grb foreground slide of our mask
        fg_mask = grb_mask[i : i + foreground_bins_number]

        # check if at least half of the foreground bins contain a GRB (1)
        if fg_mask.mean()>=0.5:
            y.append(1)
        else:
            y.append(0)

    return np.array(y)

def generate_dataset(n_orbits=50, n_bins=1000):
    """
    Simulate n_orbits separate CubeSat orbits in a loop, where each orbit generates its own X_orbit and y_orbit with length `(n_bins - background_bins_number - foreground_bins_number + 1)`.

    Parameters
    ----------
    n_orbits : int, default 50
        Number of separate orbits to simulate.
    n_bins : int, default 1000
        Number of bins in an orbit, each bin is a photon count recording.

    Returns
    -------
    X_orbit : numpy.ndarray (n, 7)
        The feature matrix compiled with the results of the
        simulation module
    y_orbit : numpy.ndarray (n, )
        The target array with the information returned by generate_labels

    Raises
    ------

    Notes
    -----
    Each orbit has a signal with length n_bins.

    The length each orbit signal after applying the background
    and foreground cuts (length of the output) `n = n_bins -
    background_bins_number - foreground_bins_number + 1`.

    """


    return None
