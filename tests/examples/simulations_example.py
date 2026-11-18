import numpy as np
import matplotlib.pyplot as plt
import grb_ml.simulations as sim

# Set seed for reproducible plots
np.random.seed(42)

# 1. Generate 1,000 bins (100 seconds at 0.1s resolution) of baseline background
n_bins = 1000
bkg = sim.generate_background(n_bins=n_bins, lam_low=40, lam_high=15)

# 2. Generate the three distinct signal types
saa_signal = sim.generate_saa_crossing(duration_bins=300, amplitude=50, hardness_ratio=0.4)
cosmic_ray = sim.generate_false_alarm(duration_bins=2, amplitude=160)
grb_signal = sim.generate_grb_pulse(
    duration_bins=120, amplitude=90, tau_rise=2.0, tau_decay=25.0, hardness_ratio=1.6
)

# 3. Package events into the list of dictionaries expected by detector_counts
events = [
    {"signal": saa_signal, "start_bin": 100, "type": "SAA Crossing", "is_grb": 0},
    {"signal": cosmic_ray, "start_bin": 520, "type": "Cosmic Ray", "is_grb": 0},
    {"signal": grb_signal, "start_bin": 700, "type": "Real GRB", "is_grb": 1},
]

# 4. Inject all events into the background timeline
counts_low, counts_high = sim.detector_counts(bkg, events)
time_sec = np.arange(n_bins) * 0.1

# 5. Plot both energy channels and annotate each injected event
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 6), sharex=True)

ax1.plot(time_sec, counts_low, color="seagreen", lw=1.0, label="Low Energy (25–100 keV)")
ax2.plot(time_sec, counts_high, color="crimson", lw=1.0, label="High Energy (100–300 keV)")

event_colors = {"SAA Crossing": "royalblue", "Cosmic Ray": "darkorange", "Real GRB": "purple"}
for ev in events:
    start_t = ev["start_bin"] * 0.1
    end_t = (ev["start_bin"] + len(ev["signal"][0])) * 0.1
    color = event_colors[ev["type"]]
    
    for ax in (ax1, ax2):
        ax.axvspan(start_t, end_t, color=color, alpha=0.18, label=ev["type"])

ax1.set_title("Simulated CubeSat Detector Timeline: SAA, Cosmic Ray, and Real GRB")
ax1.set_ylabel("Counts / 0.1s bin")
ax1.legend(loc="upper left")

ax2.set_xlabel("Time (seconds)")
ax2.set_ylabel("Counts / 0.1s bin")
ax2.legend(loc="upper left")

plt.tight_layout()
plt.show()
