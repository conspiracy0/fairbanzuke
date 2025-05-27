import csv


def import_weight_chart(filename):
    with open(filename, mode='r', newline='', encoding='utf-8') as file:
        ranks = ['y','o','s','k'] + [f'm{i}' for i in range(1,19)]
        reader = list(csv.DictReader(file))  # turn reader into a list so we can index
        win_percent_dict = {}

        for idx, row in enumerate(reader):
            if row["Rank vs"] == "Total Matches":
                continue

            current_rank = row["Rank vs"].lower()
            i = ranks.index(current_rank)

            info = {}
            for opp_rank in ranks[i+1:]:
                info[opp_rank] = [row[opp_rank]]

            # get the corresponding "Total Matches" row
            if idx + 1 < len(reader) and reader[idx + 1]["Rank vs"] == "Total Matches":
                match_row = reader[idx + 1]
                for opp_rank in ranks[i+1:]:
                    info[opp_rank].append(match_row[opp_rank])

            # store it if needed
            win_percent_dict[current_rank] = info

        # print(win_percent_dict)
        for rank in win_percent_dict:
            total_weighted = 0.0
            total_matches = 0

            for opp_rank, (win_str, match_str) in win_percent_dict[rank].items():
                try:
                    win = float(win_str)
                    matches = int(match_str)
                    if matches > 0:
                        total_weighted += win * matches
                        total_matches += matches
                except ValueError:
                    # skip 'N/A' or bad data
                    continue

            if total_matches > 0:
                weighted_mean = total_weighted / total_matches
            else:
                weighted_mean = None

            print(f"{rank}:totalmatches: {total_matches} WWOF = {weighted_mean:.4f}" if weighted_mean is not None else f"{rank}: WWOF = N/A")

#      with open(filename, mode='r', newline='', encoding='utf-8') as file:
#         # list of all ranks in order
#         ranks = ['y','o','s','k'] + [f'm{i}' for i in range(1,19)]
#         reader = csv.DictReader(file)
#         win_percent_dict = {}
#         for row in reader:
#             if row["Rank vs"] != "Total Matches":
#
#                 current_rank = row["Rank vs"].lower()
#
#                 info = {}
#                 i = ranks.index(current_rank)
#                 for opp_rank in ranks[i+1:]:
#                     info[opp_rank] = [row[opp_rank]]
#                 # print(info)
#                 for row+1
#                 win_percent_dict[current_rank] = info
#
#
#

import_weight_chart("all_ranks_head_to_head.csv")
# # compute wwof for each rank
# for idx, rank in enumerate(ranks):
#     lower_ranks = ranks[idx+1:]
#     num = 0.0
#     den = 0
#     for opp in lower_ranks:
#         p = percent.get(opp)
#         m = matches.get(opp, 0)
#         if p is not None and m > 0:
#             num += p * m
#             den += m
#     wwof[rank] = (num/den) if den else None
#
# # output
# for rank in ranks:
#     print(f"{rank}: {wwof[rank]}")
