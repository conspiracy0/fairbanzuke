import csv

# Ordered rank list
all_ranks = (
    [f"s{i}{side}" for i in range(1, 4) for side in ["e", "w"]] +
    [f"k{i}{side}" for i in range(1, 4) for side in ["e", "w"]] +
    [f"m{i}{side}" for i in range(1, 19) for side in ["e", "w"]] +
    [f"j{i}{side}" for i in range(1, 15) for side in ["e", "w"]]
)

input_file = "filtered_rank_change_results.csv"

# rank → win_count → { total_diff, total_matches }
detailed_stats = {
    rank: {w: {"total_diff": 0, "total_matches": 0} for w in range(16)}
    for rank in all_ranks
}

grand_total_diff = 0
grand_total_matches = 0

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
            end_idx = all_ranks.index(end_rank)
        except ValueError:
            continue

        expected_delta = (2 * wins) - 15
        expected_idx = max(0, min(len(all_ranks) - 1, start_idx - expected_delta))

        signed_diff = end_idx - expected_idx

        slot = detailed_stats[start_rank][wins]
        slot["total_diff"] += signed_diff * matches
        slot["total_matches"] += matches

        grand_total_diff += signed_diff * matches
        grand_total_matches += matches

# Output
print("Rank → Win Count → Avg Divergence")
total_avg_of_avgs = 0
rank_with_data_count = 0

for rank in all_ranks:
    total_diff = 0
    total_matches = 0
    print(f"\n{rank}:")

    for wins in range(16):
        data = detailed_stats[rank][wins]
        if data["total_matches"] == 0:
            continue
        diff = data["total_diff"]
        matches = data["total_matches"]
        avg = diff / matches
        print(f"  Wins {wins:2}: {avg:+.3f}, (num={matches})")
        total_diff += diff
        total_matches += matches

    if total_matches > 0:
        rank_avg = total_diff / total_matches
        print(f"  → Rank Weighted Avg: {rank_avg:+.3f}")
        total_avg_of_avgs += rank_avg * total_matches
        rank_with_data_count += total_matches


# Final overall averages
overall_avg_of_avgs = total_avg_of_avgs / rank_with_data_count if rank_with_data_count else 0

overall_weighted_avg = grand_total_diff / grand_total_matches if grand_total_matches else 0

print("\n=== Summary ===")
print(f"Average of Rank Averages: {overall_avg_of_avgs:+.3f}")
print(f"Weighted Global Average Divergence: {overall_weighted_avg:+.3f}")
