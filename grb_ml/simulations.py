import numpy as np

def generate_background(n_bins, lam_low=40, lam_high=15):
    """
    Generates background radiation noise with Poisson distribution.

    Args:
        n_bins (int): number of times bins with lam_low+lam_high counts each
        lam_low (int): average rate of the low-energy channel
        lam_high (int): average rate of the high-energy channel

    Returns:
        Tuple of 2 NumPy Arrays (each shape (n_bins,))
    """

    if lam_low<0:
        raise ValueError("Low-energy channel average counts must be positive or zero.")
    if lam_high<0:
        raise ValueError("High-energy channel average counts must be positive or zero.")

    low_background = np.random.poisson(lam=lam_low, size=n_bins)
    high_background = np.random.poisson(lam=lam_high, size=n_bins)

    return (low_background, high_background)


def generate_grb_pulse(duration_bins, amplitude, tau_rise=2.0, tau_decay=20.0, hardness_ratio=1.5):
    """
    Generates the photon count rate of a GRB signal.

    Args:
        duration_bins (int) duration of the signal
        amplitude (int): peak count rate
        tau_rise (float): rise time constant
        tau_decay (float): decay time constant
        hardness_ratio (float): ratio high_counts/low_counts

    Returns:
        Tuple of 2 NumPy Arrays (each shape (duration_bins,))
    """

    if duration_bins<=0:
        raise ValueError("Duration of the bins must be positive.")
    if amplitude<=0:
        raise ValueError("GRB Pulse amplitude must be positive.")
    if tau_rise>tau_decay:
        raise ValueError("tau_rise cannot be larger than tau_decay (or they invert roles in the rate equation.)")
    if hardness_ratio<1.0 or hardness_ratio>2.5:
        raise ValueError("hardness_ratio is outside physical constraints (1.0<HR<2.5)")

    t = np.arange(duration_bins)

    rise_term = 1-np.exp(-t / tau_rise)
    decay_term = np.exp(-t / tau_decay)

    rate_curve = amplitude * rise_term * decay_term

    # spectral evolution
    # high-energy photons decay slightly faster
    # this happens in real GRBs because the fireball cools down
    decay_term_high_channel = np.exp(-t / (tau_decay * 0.8))
    rate_curve_high = amplitude * rise_term * decay_term_high_channel

    # hardness ratio
    rate_curve_low = rate_curve
    rate_curve_high = hardness_ratio * rate_curve_low

    low_counts = np.random.poisson(lam=rate_curve_low)
    high_counts = np.random.poisson(lam=rate_curve_high)

    return (low_counts, high_counts)



def generate_false_alarm(duration_bins=2, amplitude=150):
    """
    Generates a short, sharp false alarm spike (e.g., cosmic ray hit).

    Args:
        duration_bins (int): very short duration (1-2 bins)
        amplitude (int): peak count rate

    Returns:
        Tuple of 2 NumPy Arrays (low and high channels)
    """

    if duration_bins<=0:
        raise ValueError("Duration of bins (time) must be positive.")
    if amplitude<=0:
        raise ValueError("Amplitude must be positive.")

    spike_rate = np.zeros(duration_bins)
    spike_rate[:] = amplitude * np.random.uniform(0.8, 1.2)

    # False alarms usually have less distinct energy constant than true GRBs
    low_spike = np.random.poisson(lam=spike_rate)
    high_spike = np.random.poisson(lam=spike_rate * 1.1)

    return (low_spike, high_spike)



def generate_saa_crossing(duration_bins=300, amplitude=60, hardness_ratio=0.4):
    """
    Generates a slow, symmetric radiation belt crossing (e.g., South Atlantic Anomaly).

    Args:
        duration_bins (int): duration of the crossing in bins
        amplitude (int): peak count rate in the low-energy channel
        hardness_ratio (float): ratio high_counts/low_counts (typically soft, < 1.0)

    Returns:
        Tuple of 2 NumPy Arrays (low and high channels, each shape (duration_bins,))
    """
    if duration_bins <= 0:
        raise ValueError("Duration of the bins must be positive.")
    if amplitude <= 0:
        raise ValueError("Amplitude must be positive.")
    if hardness_ratio <= 0 or hardness_ratio > 1.0:
        raise ValueError("SAA hardness_ratio should be soft (0.0 < HR <= 1.0).")

    t = np.arange(duration_bins)

    # Half-sine wave from 0 to pi: starts at 0, peaks at amplitude, ends at 0
    rate_curve_low = amplitude * np.sin(np.pi * t / duration_bins)
    rate_curve_high = hardness_ratio * rate_curve_low

    low_counts = np.random.poisson(lam=rate_curve_low)
    high_counts = np.random.poisson(lam=rate_curve_high)

    return (low_counts, high_counts)




# injecting everything into a single detector signal

def detector_counts(bkg, events):
    """
    Injects events (GRB pulse, cosmic ray, SSA, ...) into a background time series on the interval start_bin to start_bin+event_duration for n events.

    Args:
        bkg (Array Tuple): Background coutns Tuple of 2 NumPy Array (low and high channels)
        events (List of Dictionaries): With the structure:
        events = [
            {"signal": (Array Tuple), "start_bin": (int), "type": (string; grb, cosmic_ray, or grb), "is_grb": (int; 0 or 1)}
        ]

    Returns:
        Tuple of 2 Arrays with the size of the background input with the injected events.
    """
    
    if len(events)==0:
        raise ValueError("Length of the events array must be larger than 0.")


    # checks

    # 1. check bkg low and high are the same length
    # 2. check low and high for each even is same length
    # 3. length of background-start_bin is larger than signal for every event

    bkg_low, bkg_high = bkg

    # check 1
    if len(bkg_low)!=len(bkg_high):
        raise ValueError(f"Length of low-energy channel background counts {len(bkg_low)} is not equal to length of high-energy channel background counts {len(bkg_high)}")


    counts_low = bkg_low.copy()
    counts_high = bkg_high.copy()

    for i, event in enumerate(events):
        event_low, event_high = event["signal"]
        start_bin = event["start_bin"]

        if len(event_low)!=len(event_high):
            raise ValueError(f"Length of the low-energy channel array {len(event_low)} is not equal to the length of the high-energy channel array {len(event_high)} (event type: {event['type']}, event id: {i})")

        if len(bkg_low)-start_bin < len(event_low):
            raise ValueError(f"Length of background remaining after starting bin (start_bin={start_bin}) must be larger than length of the event counts ({len(event_low)}). Currently is {len(bkg_low)-start_bin}. (event type: {event['type']}, event id: {i})")

        if start_bin <= 0:
            raise ValueError(f"start_bin must be positive.")

        end_bin = start_bin + len(event_low)

        counts_low[start_bin:end_bin] += event_low
        counts_high[start_bin:end_bin] += event_high

    return (counts_low, counts_high)

