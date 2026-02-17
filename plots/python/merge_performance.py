import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# ===============================
# MERGE PERFORMANCE (FIRST MERGE)
# ===============================

# number of concurrent appenders
concurrency_levels = np.array([1, 2, 5, 10])

# merge times for 4KiB appends (ms)
merge_4K_trials = [
    [72, 75, 70, 74, 73],      # 1 client
    [95, 100, 92, 97, 96],     # 2 clients
    [155, 160, 150, 158, 156], # 5 clients
    [230, 245, 240, 235, 238]  # 10 clients
]

# merge times for 32KiB appends (ms)
merge_32K_trials = [
    [110, 115, 112, 114, 111],  # 1 client
    [160, 155, 165, 162, 158],  # 2 clients
    [255, 260, 250, 257, 254],  # 5 clients
    [410, 425, 420, 415, 418]   # 10 clients
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

mean_4K, std_4K, err_low_4K, err_high_4K = summarize_trials(merge_4K_trials)
mean_32K, std_32K, err_low_32K, err_high_32K = summarize_trials(merge_32K_trials)

# ===============================
# PLOTTING
# ===============================

plt.figure(figsize=(10, 6))
plt.errorbar(concurrency_levels, mean_4K, yerr=[err_low_4K, err_high_4K], fmt='-o', capsize=5, label='4 KiB appends')
plt.errorbar(concurrency_levels, mean_32K, yerr=[err_low_32K, err_high_32K], fmt='-o', capsize=5, label='32 KiB appends', color='orange')

plt.title("Merge Time vs. Number of Concurrent Appends")
plt.xlabel("Number of Concurrent Appends (j)")
plt.ylabel("Merge Completion Time (ms)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("merge_performance_plot.png", dpi=300)
plt.show()