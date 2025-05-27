import csv

# define ranks in order
ranks = ['y','o','s','k'] + [f'm{i}' for i in range(1,19)] + [f"j{i}" for i in range(1, 15)]

# read entire file into a list so we can peek at "Total Matches" rows
with open('all_ranks_head_to_head.csv', mode='r', newline='', encoding='utf-8') as infile:
	reader = list(csv.DictReader(infile))

# build two lookup tables:
#  - all_data[rank]   = {opp_rank: (win_ratio, matches), ...} for every opponent
#  - lower_data[rank] = same, but only for opponents lower in 'ranks'
all_data = {}
lower_data = {}

for idx, row in enumerate(reader):
	if row["Rank vs"] == "Total Matches":
		continue
	rank = row["Rank vs"].lower()
	i = ranks.index(rank)
	match_row = reader[idx + 1]

	info_all = {}
	info_lower = {}

	for opp in ranks:
		if opp == rank:
			continue
		win_str = row.get(opp, 'N/A')
		matches_str = match_row.get(opp, '0')
		info_all[opp] = (win_str, matches_str)
		# only keep lower-ranked for WWOF
		if opp in ranks[i+1:]:
			info_lower[opp] = (win_str, matches_str)

	all_data[rank] = info_all
	lower_data[rank] = info_lower

# now write out one CSV
with open('rikishi_full_summary.csv', mode='w', newline='', encoding='utf-8') as outfile:
	fieldnames = [
		'Rank','Opponent Rank',
		'Wins','Losses','Total Matches',
		'Win/Loss Ratio','WWOF','Win%'
	]
	writer = csv.DictWriter(outfile, fieldnames=fieldnames)
	writer.writeheader()

	for rank in ranks:
		data_all   = all_data.get(rank, {})
		data_lower = lower_data.get(rank, {})

		# accumulators for summary across all fights
		sum_wins_all       = 0.0
		sum_losses_all     = 0.0
		sum_matches_all    = 0
		sum_ratio_wt_all   = 0.0
		sum_winpct_wt_all  = 0.0

		# accumulators for WWOF (only lower fights)
		sum_ratio_wt_low   = 0.0
		sum_matches_low    = 0

		# per-matchup rows (all opponents)
		for opp, (wr_str, m_str) in data_all.items():
			try:
				ratio   = float(wr_str)
				matches = int(m_str)
				if matches == 0:
					continue

				# back out wins/losses
				losses = matches / (ratio + 1)
				wins   = matches - losses
				winpct = wins / matches

				# write the row
				writer.writerow({
					'Rank': rank,
					'Opponent Rank': opp,
					'Wins': round(wins),
					'Losses': round(losses),
					'Total Matches': matches,
					'Win/Loss Ratio': round(ratio, 4),
					'WWOF': '',            # only in summary
					'Win%': round(winpct, 4)
				})

				# accumulate for overall summary
				sum_wins_all      += wins
				sum_losses_all    += losses
				sum_matches_all   += matches
				sum_ratio_wt_all  += ratio * matches
				sum_winpct_wt_all += winpct * matches

				# if it's a lower-ranked opponent, accumulate for WWOF
				if opp in data_lower:
					sum_ratio_wt_low += ratio * matches
					sum_matches_low  += matches

			except (ValueError, ZeroDivisionError):
				continue

		# compute summary metrics
		summary_ratio = (sum_ratio_wt_all  / sum_matches_all)  if sum_matches_all else None
		summary_winpct= (sum_winpct_wt_all/ sum_matches_all)  if sum_matches_all else None
		summary_wwof = (sum_ratio_wt_low/ sum_matches_low)    if sum_matches_low  else None

		# write the final "ALL" row for this rank
		writer.writerow({
			'Rank': rank,
			'Opponent Rank': 'ALL',
			'Wins': round(sum_wins_all),
			'Losses': round(sum_losses_all),
			'Total Matches': sum_matches_all,
			'Win/Loss Ratio': round(summary_ratio, 4) if summary_ratio is not None else 'N/A',
			'WWOF': round(summary_wwof, 4)          if summary_wwof  is not None else 'N/A',
			'Win%': round(summary_winpct,4)         if summary_winpct is not None else 'N/A'
		})
