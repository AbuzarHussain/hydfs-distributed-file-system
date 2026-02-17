import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# X = number of files (each 128 KiB)
file_counts = np.array([10, 50, 100, 200])

# total bandwidth (in bytes or MB) for each trial per X
bandwidth_trials = [
    [2.5, 1.87, 3, 3.13, 2.75],      # 10 files
    [10, 11, 11.25, 10.62, 9.5],   # 50 files
    [19, 20.63, 21.5, 17.5, 17.38],   # 100 files
    [41, 37.75, 39, 44.37, 39.38]    # 200 files
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

bw_mean, bw_std, bw_err_low, bw_err_high = summarize_trials(bandwidth_trials)

# ===============================
# PLOTTING
# ===============================

plt.figure(figsize=(10, 6))
plt.errorbar(file_counts, bw_mean, yerr=[bw_err_low, bw_err_high], fmt='-o', capsize=5, color='purple')
plt.title("Rebalance Bandwidth vs. Number of Files")
plt.xlabel("Number of Files (X)")
plt.ylabel("Bandwidth Used (MiB)")
plt.grid(True)
plt.tight_layout()
plt.savefig("rebalance_bandwidth_plot.png", dpi=300)
plt.show()