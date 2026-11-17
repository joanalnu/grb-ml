import numpy as np

def generate_labels(n_bins, events, background_bins_number=100, foreground_bins_number=10):
    """
    Produces the 1D target array mathing the exact rows returned by features.feature_extraction_loop().\\

    Args:\\
        - n_bins (int): number of bins of ...\\
        - events (list of dictionaries): with the structure events = [{"signal": (Array Tuple), "start_bin": (int), "type": (string; grb, cosmic_ray, or grb), "is_grb": (int; 0 or 1)}]\\
        - background_bins_number (int): set to 100 by default\\
        - foreground_bins_number (int): set to 10 by default\\

    Returns:
        - y (1D array): the target column (is_grb), if more than half of the bins are is_grb true
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
    Simulate n_orbits separate CubeSat orbits in a loop, where each orbit generates its own X_orbit and y_orbit with length (n_bins - background_bins_number - foreground_bins_number + 1).

    Args:
        - n_orbits: ...
        - n_bins: ...

    Returns:
        ...
    """


    return None
