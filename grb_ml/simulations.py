import numpy as np

def generate_background(n_bins, lam_low=40, lam_high=15):
    """
    Generate Poisson background counts for both energy channels.

    Parameters
    ----------
    n_bins : int
        Number of time bins.
    lam_low : float, default 40
        Mean count per bin, low-energy channel.
    lam_high : float, default 15
        Mean count per bin, high-energy channel.

    Returns
    -------
    low, high : numpy.ndarray, shape (n_bins,)
        Background counts per channel.

    Raises
    ------
    ValueError
        If a rate is negative.

    Examples
    --------
    >>> low, high = generate_background(1000)
    >>> low.shape
    (1000,)
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
    Generate a GRB pulse with a fast rise and exponential decay.

    Parameters
    ----------
    duration_bins : int
        Duration of the pulse in bins.
    amplitude : float
        Peak count rate of the low channel.
    tau_rise : float, default 2.0
        Rise time constant.
    tau_decay : float, default 20.0
        Decay time constant (must be >= `tau_rise`).
    hardness_ratio : float, default 1.5
        High/low channel rate ratio, in [1.0, 2.5].

    Returns
    -------
    low, high : numpy.ndarray, shape (duration_bins,)
        Poisson-sampled counts per channel.

    Raises
    ------
    ValueError
        If an argument is outside its allowed range.

    Notes
    -----
    The low-channel rate is

    .. math:: r(t) = A\\,(1 - e^{-t/\\tau_r})\\,e^{-t/\\tau_d}

    and the high channel is ``hardness_ratio * r(t)``.
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
    Generate a short, sharp spike mimicking a cosmic-ray hit.

    Parameters
    ----------
    duration_bins : int, default 2
        Duration of the spike in bins.
    amplitude : float, default 150
        Nominal peak count rate (randomly scaled by 0.8-1.2).

    Returns
    -------
    low, high : numpy.ndarray, shape (duration_bins,)
        Counts per channel; the high channel is ~1.1x the low channel.

    Raises
    ------
    ValueError
        If `duration_bins` or `amplitude` is not positive.
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
    Generate a slow, symmetric South Atlantic Anomaly crossing.

    Parameters
    ----------
    duration_bins : int, default 300
        Duration of the crossing in bins.
    amplitude : float, default 60
        Peak low-channel count rate.
    hardness_ratio : float, default 0.4
        High/low channel ratio, in (0, 1] (a soft spectrum).

    Returns
    -------
    low, high : numpy.ndarray, shape (duration_bins,)
        Poisson-sampled counts per channel.

    Raises
    ------
    ValueError
        If an argument is outside its allowed range.

    Notes
    -----
    The rate follows a half sine wave, :math:`A\\sin(\\pi t / T)`.
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
    Inject events into a background time series.

    Parameters
    ----------
    bkg : tuple of numpy.ndarray
        ``(low, high)`` background counts.
    events : list of dict
        Each dict has the keys ``"signal"`` (``(low, high)`` arrays),
        ``"start_bin"`` (int, > 0), ``"type"`` (str, e.g. ``"grb"``) and
        optionally ``"is_grb"`` (0 or 1).

    Returns
    -------
    low, high : numpy.ndarray
        Copies of the background with all events added.

    Raises
    ------
    ValueError
        If `events` is empty, channel lengths differ, an event does not fit
        in the background, or ``start_bin`` is not positive.

    See Also
    --------
    generate_background
    generate_grb_pulse
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
