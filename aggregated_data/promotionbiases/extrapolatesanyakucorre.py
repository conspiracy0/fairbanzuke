import csv
import json

# full ordered rank list
all_ranks = (
	[f"s{i}{side}" for i in range(1, 4) for side in ["e", "w"]] +
	[f"k{i}{side}" for i in range(1, 4) for side in ["e", "w"]] +
	[f"m{i}{side}" for i in range(1, 19) for side in ["e", "w"]] +
	[f"j{i}{side}" for i in range(1, 15) for side in ["e", "w"]]
)

input_file = "filtered_rank_change_resultscomplete.csv"
output_file = "sanyaku_divergence.csv"

with open(input_file, newline='', encoding='utf-8') as infile, open(output_file, 'w', newline='', encoding='utf-8') as outfile:
	reader = csv.reader(infile)
	writer = csv.writer(outfile)

	# write header
	writer.writerow([
		"Start Rank",
		"End Rank",
		"Wins",
		"Matches",
		"Avg Weighted Sanyaku Score",
		"Signed Divergence"
	])

	next(reader)  # skip header

	for row in reader:
		# skip separators and total rows
		if row[0] == "#" or row[2] == "TOTAL":
			continue

		start_rank = row[0]
		end_rank   = row[1]
		wins       = int(row[2])
		matches    = int(row[3])
		sanyaku_json = row[4]

		if matches == 0 or not sanyaku_json:
			continue

		try:
			start_idx = all_ranks.index(start_rank)
			end_idx   = all_ranks.index(end_rank)
		except ValueError:
			continue  # unrecognized rank

		# compute expected index
		expected_delta = (2 * wins) - 15
		expected_idx = start_idx - expected_delta
		if expected_idx < 0:
			expected_idx = 0
		elif expected_idx >= len(all_ranks):
			expected_idx = len(all_ranks) - 1

		signed_diff = end_idx - expected_idx

		# load sanyaku results list of dicts
		try:
			sanyaku_data = json.loads(sanyaku_json)
		except json.JSONDecodeError:
			continue

		# compute total weighted sanyaku score
		score_total = 0
		for result in sanyaku_data:
			y = result.get("y", 0)
			o = result.get("o", 0)
			s = result.get("s", 0)
			k = result.get("k", 0)
			score_total += (4 * y + 3 * o + 2 * s + 1 * k)

		# average per wrestler
		avg_sanyaku_score = score_total / matches

		# write output row
		writer.writerow([
			start_rank,
			end_rank,
			wins,
			matches,
			f"{avg_sanyaku_score:.3f}",
			signed_diff
		])
