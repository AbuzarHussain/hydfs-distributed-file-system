import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# File sizes (in KiB)
file_sizes = np.array([1, 10, 100, 512, 1024])

# Re-replication times for 5 trials per file size (in milliseconds)
rereplication_time_trials = [
    [7, 8, 7, 9, 8],   # 1 KiB
    [43, 44, 45, 45, 44],   # 10 KiB
    [54, 58, 45, 45, 49],   # 100 KiB
    [50, 49, 52, 53, 65],   # 512 KiB
    [78, 70, 69, 72, 70]  # 1 MiB
]

# Bandwidth usage for 5 trials per file size (in MiB)
bandwidth_trials = [
    [0.22, 0.19, 0.25, 0.24, 0.34],  # 1 KiB
    [2.62, 2.07, 2.54, 2.66, 2.61],  # 10 KiB
    [7.42, 36.43, 31.44, 37.57, 30.27],  # 100 KiB
    [135, 157, 165.5, 170.5, 220],  # 512 KiB
    [136, 321, 377, 455, 415]  # 1 MiB
]

# ===============================
# CALCULATIONS
# ===============================

def summarize_trials(trials):
    means = [np.mean(t) for t in trials]
    stds = [np.std(t, ddof=1) for t in trials]
    conf_intervals = [stats.t.interval(0.95, len(t)-1, loc=np.mean(t), scale=stats.sem(t)) for t in trials]
    lower_bounds = [mean - ci[0] for mean, ci in zip(means, conf_intervals)]
    upper_bounds = [ci[1] - mean for mean, ci in zip(means, conf_intervals)]
    return np.array(means), np.array(stds), np.array(lower_bounds), np.array(upper_bounds)

time_mean, time_std, time_err_low, time_err_high = summarize_trials(rereplication_time_trials)
bw_mean, bw_std, bw_err_low, bw_err_high = summarize_trials(bandwidth_trials)

# ===============================
# PLOTTING
# ===============================

plt.figure(figsize=(10, 5))

# Plot 1 — Re-replication Time
plt.errorbar(file_sizes, time_mean, yerr=[time_err_low, time_err_high], fmt='-o', capsize=5, label='Re-replication Time')
plt.title("Re-replication Time vs. File Size")
plt.xlabel("File Size (KiB)")
plt.ylabel("Time (ms)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("rereplication_time_plot.png", dpi=300)
plt.show()

# Plot 2 — Bandwidth
plt.figure(figsize=(10, 5))
plt.errorbar(file_sizes, bw_mean, yerr=[bw_err_low, bw_err_high], fmt='-o', color='orange', capsize=5, label='System-wide Bandwidth')
plt.title("System-wide Bandwidth vs. File Size")
plt.xlabel("File Size (KiB)")
plt.ylabel("Bandwidth (MiB transferred)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("bandwidth_plot.png", dpi=300)
plt.show()