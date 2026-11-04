from grb_ml import *
import matplotlib.pyplot as plt

# 1. Generate 1000 bins of background and a 100-bin GRB pulse
bkg = generate_background(n_bins=1000, lam_low=40, lam_high=15)
grb = generate_grb_pulse(duration_bins=100, amplitude=80, tau_rise=2.0, tau_decay=20.0, hardness_ratio=1.5)

# 2. Inject the GRB at bin 300 (t = 30.0 seconds)
counts_low, counts_high = detector_counts(bkg, grb, start_bin=300)
time_sec = np.arange(1000) * 0.1

# 3. Plot the two energy channels
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True)

ax1.plot(time_sec, counts_low, color="seagreen", label="Low Energy (25–100 keV)")
ax1.axvline(30.0, color="black", linestyle="--", alpha=0.6, label="GRB Trigger (30s)")
ax1.set_ylabel("Counts / 0.1s bin")
ax1.legend(loc="upper right")
ax1.set_title("Simulated CubeSat GRB Light Curve")

ax2.plot(time_sec, counts_high, color="crimson", label="High Energy (100–300 keV)")
ax2.axvline(30.0, color="black", linestyle="--", alpha=0.6)
ax2.set_xlabel("Time (seconds)")
ax2.set_ylabel("Counts / 0.1s bin")
ax2.legend(loc="upper right")

plt.tight_layout()
plt.show()
