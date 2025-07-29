import os
import csv

import numpy as np
folder = "../fairbanzukeoutput"  # replace with your actual folder name

total_sum = []
for fname in os.listdir(folder):
    if not fname.endswith(".csv"):
        continue
    path = os.path.join(folder, fname)
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        signed_diffs = []
        for row in reader:
            if "M" in row["New Rank Title"] and "M" in row["Old Rank Title"]:
                # signed_diff_sum += int(row["Signed Diff"])
                signed_diffs.append(int(row["Signed Diff"]))
#

        print(fname, sum(signed_diffs))
        total_sum.append(signed_diffs)

# folder = "../fairbanzukeoutputnofixes"
folder = "../fairbanzukeoutputjuryobias"
raw_total_sum = []
used_basho_codes = []
print("Starting nofixes")
for fname in os.listdir(folder):
    if not fname.endswith(".csv"):
        continue
    path = os.path.join(folder, fname)
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        # signed_diff_sum = 0
        # abs
        signed_diffs = []
        for row in reader:
            if "M" in row["New Rank Title"] and "M" in row["Old Rank Title"]:
                # signed_diff_sum += int(row["Signed Diff"])
                signed_diffs.append(int(row["Signed Diff"]))
#

        print(fname, sum(signed_diffs))
        raw_total_sum.append(signed_diffs)
        used_basho_codes.append(f"{fname[:-11]}")


# print("Raw total sum:", raw_total_sum, "Heuristic total sum: ", total_sum)
import statistics

def print_stats(title, data):
    print(f"{title}:")
    print(f"    {'Lowest val:':<20}{min(data):<10} {'Highest val:':<15}{max(data):<10}")
    print(f"    {'Median:':<20}{statistics.median(data):<10.2f}")
    print(f"    {'Mean:':<20}{statistics.mean(data):<10.2f}")
    print(f"    {'Q1:':<20}{np.percentile(data, 25):<10.2f} {'Q3:':<15}{np.percentile(data, 75):<10.2f}")

print_stats("juryo bias", [sum(n) for n in raw_total_sum])
# print()
print_stats("Heuristic", [sum(n) for n in total_sum])

print_stats("juryo bias abs ", [sum([abs(x) for x in n]) for n in raw_total_sum])
print()
print_stats("Heuristic abs", [sum([abs(x) for x in n]) for n in total_sum])



all_tourney_stats = []

for values in total_sum:
	stats = {
		"min": min(values),
		"max": max(values),
		"mean": statistics.mean(values),
		"median": statistics.median(values),
		"q1": np.percentile(values, 25),
		"q3": np.percentile(values, 75),
	}
	all_tourney_stats.append(stats)

stat_keys = ["min", "max", "mean", "median", "q1", "q3"]
all_stats_by_type = {k: [stats[k] for stats in all_tourney_stats] for k in stat_keys}

# Now print stats of stats:
print("Stats of Each Stat Across All Tournaments (Fixes)")

for stat in stat_keys:
	values = [stats[stat] for stats in all_tourney_stats]

	# Find indexes for min and max
	min_val = min(values)
	max_val = max(values)
	min_idx = values.index(min_val)
	max_idx = values.index(max_val)
	min_code = used_basho_codes[min_idx]
	max_code = used_basho_codes[max_idx]

	# Compute median, Q1, Q3 values and find their closest actual values
	median_val = statistics.median(values)
	q1_val = np.percentile(values, 25)
	q3_val = np.percentile(values, 75)

	# Find index of closest value for median, q1, q3, mean (to get the corresponding basho code)
	def closest_idx(val):
		return min(range(len(values)), key=lambda i: abs(values[i] - val))

	median_idx = closest_idx(median_val)
	q1_idx = closest_idx(q1_val)
	q3_idx = closest_idx(q3_val)
	mean_val = statistics.mean(values)
	mean_idx = closest_idx(mean_val)

	print(f"\n{stat.title()}:")
	print(f"    Lowest:  {min_val:.2f}  (basho {used_basho_codes[min_idx]})")
	print(f"    Highest: {max_val:.2f}  (basho {used_basho_codes[max_idx]})")
	print(f"    Mean:    {mean_val:.2f}  (closest basho {used_basho_codes[mean_idx]})")
	print(f"    Median:  {median_val:.2f}  (closest basho {used_basho_codes[median_idx]})")
	print(f"    Q1:      {q1_val:.2f}  (closest basho {used_basho_codes[q1_idx]})")
	print(f"    Q3:      {q3_val:.2f}  (closest basho {used_basho_codes[q3_idx]})")


all_tourney_stats = []

for values in raw_total_sum:
	stats = {
		"min": min(values),
		"max": max(values),
		"mean": statistics.mean(values),
		"median": statistics.median(values),
		"q1": np.percentile(values, 25),
		"q3": np.percentile(values, 75),
	}
	all_tourney_stats.append(stats)

stat_keys = ["min", "max", "mean", "median", "q1", "q3"]
all_stats_by_type = {k: [stats[k] for stats in all_tourney_stats] for k in stat_keys}

# Now print stats of stats:
print("Stats of Each Stat Across All Tournaments (No Fixes)")

for stat in stat_keys:
	values = [stats[stat] for stats in all_tourney_stats]

	# Find indexes for min and max
	min_val = min(values)
	max_val = max(values)
	min_idx = values.index(min_val)
	max_idx = values.index(max_val)
	min_code = used_basho_codes[min_idx]
	max_code = used_basho_codes[max_idx]

	# Compute median, Q1, Q3 values and find their closest actual values
	median_val = statistics.median(values)
	q1_val = np.percentile(values, 25)
	q3_val = np.percentile(values, 75)

	# Find index of closest value for median, q1, q3, mean (to get the corresponding basho code)
	def closest_idx(val):
		return min(range(len(values)), key=lambda i: abs(values[i] - val))

	median_idx = closest_idx(median_val)
	q1_idx = closest_idx(q1_val)
	q3_idx = closest_idx(q3_val)
	mean_val = statistics.mean(values)
	mean_idx = closest_idx(mean_val)

	print(f"\n{stat.title()}:")
	print(f"    Lowest:  {min_val:.2f}  (basho {used_basho_codes[min_idx]})")
	print(f"    Highest: {max_val:.2f}  (basho {used_basho_codes[max_idx]})")
	print(f"    Mean:    {mean_val:.2f}  (closest basho {used_basho_codes[mean_idx]})")
	print(f"    Median:  {median_val:.2f}  (closest basho {used_basho_codes[median_idx]})")
	print(f"    Q1:      {q1_val:.2f}  (closest basho {used_basho_codes[q1_idx]})")
	print(f"    Q3:      {q3_val:.2f}  (closest basho {used_basho_codes[q3_idx]})")

# # collect lists of each stat across all tournaments
# stat_keys = ["min", "max", "mean", "median", "q1", "q3"]
# all_stats_by_type = {k: [stats[k] for stats in all_tourney_stats] for k in stat_keys}

# # Now print stats of stats:
# print("Stats of Each Stat Across All Tournaments (Fixes)")
# for stat in stat_keys:
# 	values = all_stats_by_type[stat]
# 	print(f"\n{stat.title()}:")
# 	print(f"    Lowest: {min(values):.2f}")
# 	print(f"    Highest: {max(values):.2f}")
# 	print(f"    Mean: {statistics.mean(values):.2f}")
# 	print(f"    Median: {statistics.median(values):.2f}")
# 	print(f"    Q1: {np.percentile(values, 25):.2f}")
# 	print(f"    Q3: {np.percentile(values, 75):.2f}")
#
#
# all_tourney_stats = []
#
# for values in raw_total_sum:
# 	stats = {
# 		"min": min(values),
# 		"max": max(values),
# 		"mean": statistics.mean(values),
# 		"median": statistics.median(values),
# 		"q1": np.percentile(values, 25),
# 		"q3": np.percentile(values, 75),
# 	}
# 	all_tourney_stats.append(stats)
#
# # collect lists of each stat across all tournaments
# stat_keys = ["min", "max", "mean", "median", "q1", "q3"]
# all_stats_by_type = {k: [stats[k] for stats in all_tourney_stats] for k in stat_keys}
#
# # Now print stats of stats:
# print("Stats of Each Stat Across All Tournaments (No Fixes)")
# for stat in stat_keys:
# 	values = all_stats_by_type[stat]
# 	print(f"\n{stat.title()}:")
# 	print(f"    Lowest: {min(values):.2f}")
# 	print(f"    Highest: {max(values):.2f}")
# 	print(f"    Mean: {statistics.mean(values):.2f}")
# 	print(f"    Median: {statistics.median(values):.2f}")
# 	print(f"    Q1: {np.percentile(values, 25):.2f}")
# 	print(f"    Q3: {np.percentile(values, 75):.2f}")

