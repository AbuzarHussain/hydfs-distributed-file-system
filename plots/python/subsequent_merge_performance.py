import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# ===============================
# SUBSEQUENT MERGE PERFORMANCE
# ===============================

# Number of concurrent appends
concurrency_levels = np.array([1, 2, 5, 10])

# Merge times (ms) for 4KiB appends — first and second merges
merge_4K_first_trials = [
    [75, 72, 74, 76, 73],
    [100, 98, 96, 97, 99],
    [155, 160, 150, 158, 157],
    [240, 245, 238, 235, 242]
]
merge_4K_second_trials = [
    [8, 9, 10, 9, 8],
    [10, 11, 9, 10, 10],
    [12, 11, 13, 12, 12],
    [15, 14, 16, 15, 15]
]

# Merge times (ms) for 32KiB appends — first and second merges
merge_32K_first_trials = [
    [110, 112, 114, 115, 111],
    [165, 162, 160, 164, 163],
    [260, 258, 257, 259, 261],
    [420, 425, 415, 418, 422]
]
merge_32K_second_trials = [
    [10, 11, 9, 10, 10],
    [12, 13, 12, 11, 12],
    [15, 14, 16, 15, 15],
    [18, 17, 19, 18, 18]
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

# 4K
m1_4K, _, err_low_4K_1, err_high_4K_1 = summarize_trials(merge_4K_first_trials)
m2_4K, _, err_low_4K_2, err_high_4K_2 = summarize_trials(merge_4K_second_trials)
# 32K
m1_32K, _, err_low_32K_1, err_high_32K_1 = summarize_trials(merge_32K_first_trials)
m2_32K, _, err_low_32K_2, err_high_32K_2 = summarize_trials(merge_32K_second_trials)

# ===============================
# PLOTTING
# ===============================

fig, ax = plt.subplots(1, 2, figsize=(12, 5), sharey=True)

# 4 KiB
ax[0].errorbar(concurrency_levels, m1_4K, yerr=[err_low_4K_1, err_high_4K_1], fmt='-o', label='First Merge')
ax[0].errorbar(concurrency_levels, m2_4K, yerr=[err_low_4K_2, err_high_4K_2], fmt='-o', label='Second Merge')
ax[0].set_title("4 KiB Appends")
ax[0].set_xlabel("Concurrent Appends (j)")
ax[0].set_ylabel("Merge Time (ms)")
ax[0].grid(True)
ax[0].legend()

# 32 KiB
ax[1].errorbar(concurrency_levels, m1_32K, yerr=[err_low_32K_1, err_high_32K_1], fmt='-o', label='First Merge')
ax[1].errorbar(concurrency_levels, m2_32K, yerr=[err_low_32K_2, err_high_32K_2], fmt='-o', label='Second Merge')
ax[1].set_title("32 KiB Appends")
ax[1].set_xlabel("Concurrent Appends (j)")
ax[1].grid(True)
ax[1].legend()

plt.suptitle("First vs Second Merge Performance")
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig("subsequent_merge_performance.png", dpi=300)
plt.show()