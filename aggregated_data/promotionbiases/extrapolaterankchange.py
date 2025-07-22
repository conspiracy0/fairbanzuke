import csv
import json

# Import all_ranks (must match your actual rank list)
all_ranks = (
	[f"s{i}{side}" for i in range(1, 4) for side in ["e", "w"]] +
	[f"k{i}{side}" for i in range(1, 4) for side in ["e", "w"]] +
	[f"m{i}{side}" for i in range(1, 19) for side in ["e", "w"]] +
	[f"j{i}{side}" for i in range(1, 15) for side in ["e", "w"]]
)

input_file = "filtered_rank_change_results.csv"

# Maps: start_rank -> { "over": x, "under": y, "bullseye": z }
rank_summary = {rank: {"over": 0, "under": 0, "bullseye": 0} for rank in all_ranks}

with open(input_file, newline='', encoding='utf-8') as f:
	reader = csv.reader(f)
	next(reader)  # header

	for row in reader:
		if row[0] == "#" or row[2] == "TOTAL":
			continue

		start_rank = row[0]
		end_rank = row[1]
		wins = int(row[2])
		matches = int(row[3])

		if matches == 0:
			continue

		try:
			start_idx = all_ranks.index(start_rank)
			true_delta = (2 * wins) - 15
			expected_idx = start_idx - true_delta
			expected_idx = max(0, min(expected_idx, len(all_ranks) - 1))
			actual_idx = all_ranks.index(end_rank)

			if actual_idx == expected_idx:
				rank_summary[start_rank]["bullseye"] += matches
			elif actual_idx < expected_idx:
				rank_summary[start_rank]["under"] += matches
			else:
				rank_summary[start_rank]["over"] += matches
		except ValueError:
			# unexpected rank, maybe a typo or unrecognized label
			continue

# Output
total_over = total_under = total_bullseye = 0
for rank, result in rank_summary.items():
	print(f"{rank}: over={result['over']}, under={result['under']}, bullseye={result['bullseye']}")
	total_over += result["over"]
	total_under += result["under"]
	total_bullseye += result["bullseye"]

print("\n=== Totals ===")
print(f"Total Over: {total_over}")
print(f"Total Under: {total_under}")
print(f"Total Bullseyes: {total_bullseye}")
