import csv

input_file = "sanyaku_divergence.csv"

# full ordered rank list
all_ranks = (
	[f"s{i}{side}" for i in range(1, 4) for side in ["e", "w"]] +
	[f"k{i}{side}" for i in range(1, 4) for side in ["e", "w"]] +
	[f"m{i}{side}" for i in range(1, 19) for side in ["e", "w"]] +
	[f"j{i}{side}" for i in range(1, 15) for side in ["e", "w"]]
)

# initialize aggregates
start_stats = {rank: {"diff_sum": 0, "sanyaku_sum": 0, "matches": 0} for rank in all_ranks}
end_stats   = {rank: {"diff_sum": 0, "sanyaku_sum": 0, "matches": 0} for rank in all_ranks}
global_diff_sum = 0
global_sanyaku_sum = 0
global_matches = 0

# for exclusion of sanyaku-start ranks
excl_diff_sum = 0
excl_sanyaku_sum = 0
excl_matches = 0

with open(input_file, newline='', encoding='utf-8') as f:
	reader = csv.reader(f)
	next(reader)  # skip header

	for row in reader:
		start_rank    = row[0]
		end_rank      = row[1]
		matches       = int(row[3])
		avg_sanyaku   = float(row[4])
		signed_diff   = float(row[5])

		if matches == 0:
			continue

		# aggregate per start rank
		start_stats[start_rank]["diff_sum"]    += signed_diff * matches
		start_stats[start_rank]["sanyaku_sum"] += avg_sanyaku * matches
		start_stats[start_rank]["matches"]     += matches

		# aggregate per end rank
		end_stats[end_rank]["diff_sum"]    += signed_diff * matches
		end_stats[end_rank]["sanyaku_sum"] += avg_sanyaku * matches
		end_stats[end_rank]["matches"]     += matches

		# aggregate global
		global_diff_sum    += signed_diff * matches
		global_sanyaku_sum += avg_sanyaku * matches
		global_matches     += matches

		# exclude sanyaku-start ranks (s and k)
		if not start_rank.startswith(("s", "k")):
			excl_diff_sum    += signed_diff * matches
			excl_sanyaku_sum += avg_sanyaku * matches
			excl_matches     += matches

def label(diff):
	if diff > 0:
		return "(under)"
	elif diff < 0:
		return "(over)"
	else:
		return ""

# 1. weighted means per starting rank
print("=== Weighted Means per Start Rank ===")
for rank, stats in start_stats.items():
	if stats["matches"] == 0:
		continue
	mean_diff    = stats["diff_sum"] / stats["matches"]
	mean_sanyaku = stats["sanyaku_sum"] / stats["matches"]
	print(f"{rank}: mean_diff={mean_diff:.3f} {label(mean_diff)}, mean_sanyaku={mean_sanyaku:.3f}")

# 2. weighted means per ending rank
print("\n=== Weighted Means per End Rank ===")
for rank, stats in end_stats.items():
	if stats["matches"] == 0:
		continue
	mean_diff    = stats["diff_sum"] / stats["matches"]
	mean_sanyaku = stats["sanyaku_sum"] / stats["matches"]
	print(f"{rank}: mean_diff={mean_diff:.3f} {label(mean_diff)}, mean_sanyaku={mean_sanyaku:.3f}")

# 3. total weighted means of entire CSV
total_mean_diff    = global_diff_sum / global_matches if global_matches else 0
total_mean_sanyaku = global_sanyaku_sum / global_matches if global_matches else 0
print("\n=== Total Weighted Means (All Data) ===")
print(f"mean_diff={total_mean_diff:.3f} {label(total_mean_diff)}, mean_sanyaku={total_mean_sanyaku:.3f}")

# 4. total weighted means excluding sanyaku-start ranks
excl_mean_diff    = excl_diff_sum / excl_matches if excl_matches else 0
excl_mean_sanyaku = excl_sanyaku_sum / excl_matches if excl_matches else 0
print("\n=== Total Weighted Means Excluding Sanyaku-Start Ranks ===")
print(f"mean_diff={excl_mean_diff:.3f} {label(excl_mean_diff)}, mean_sanyaku={excl_mean_sanyaku:.3f}")
