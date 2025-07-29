import requests, os, math
from bs4 import BeautifulSoup
import time
import csv
from functools import cmp_to_key
class Rikishi:

    def __init__(self, name, beats):
        self.name = name
        self.beats = beats
        self.wins = len(beats)
        self.losses = 15-self.wins
        self.record = (self.wins-self.losses)*2
        # self.record = (self.wins-self.losses)
        self.neustadl = self.wins
        self.weighted_neustadl = None
        self.rank = None
        self.inverse_rank = None
        self.weight = None
        self.sanyaku = ""
        self.weighted_raw_record = 0
        self.sanyaku_out = ""
        self.starting_rank = ""
        self.new_rank_title = None

import csv

sanyakutitles = {
    "Yokozuna 1 East":	"Y1e",
    "Yokozuna 1 East Yokozuna-Ozeki": "Y1e",
	"Yokozuna 1 West":	"Y1w",
	"Yokozuna 1 West Yokozuna-Ozeki": "Y1w",
	"Yokozuna 2 East":	"Y2e",
	"Yokozuna 2 East Yokozuna-Ozeki": "Y2e",
	"Yokozuna 2 West":	"Y2w",
	"Yokozuna 2 West Yokozuna-Ozeki": "Y2w",
	"Yokozuna 3 East":	"Y3e",
	"Yokozuna 3 West":	"Y3w",

	"Ozeki 1 East":	"O1e",
	"Ozeki 1 West":	"O1w",
	"Ozeki 2 East":	"O2e",
	"Ozeki 2 West":	"O2w",
	"Ozeki 3 East":	"O3e",
	"Ozeki 3 West":	"O3w",

	"Sekiwake 1 East":	"S1e",
	"Sekiwake 1 West":	"S1w",
	"Sekiwake 2 East":	"S2e",
	"Sekiwake 2 West":	"S2w",
	"Sekiwake 3 East":	"S3e",
	"Sekiwake 3 West":	"S3w",

	"Komusubi 1 East":	"K1e",
	"Komusubi 1 West":	"K1w",
	"Komusubi 2 East":	"K2e",
	"Komusubi 2 West":	"K2w",
	"Komusubi 3 East":	"K3e",
	"Komusubi 3 West":	"K3w",

	# Haridashi (overflow) mapping
	"Yokozuna 1 East Haridashi":	"Y1e",
	"Yokozuna 1 West Haridashi":	"Y1w",
	"Yokozuna 2 East Haridashi":	"Y2e",
	"Yokozuna 2 West Haridashi":	"Y2w",
	"Yokozuna 3 East Haridashi":	"Y3e",
	"Yokozuna 3 West Haridashi":	"Y3w",

	"Ozeki 1 East Haridashi":	"O1e",
	"Ozeki 1 West Haridashi":	"O1w",
	"Ozeki 2 East Haridashi":	"O2e",
	"Ozeki 2 West Haridashi":	"O2w",
	"Ozeki 3 East Haridashi":	"O3e",
	"Ozeki 3 West Haridashi":	"O3w",

	"Sekiwake 1 East Haridashi":	"S1e",
	"Sekiwake 1 West Haridashi":	"S1w",
	"Sekiwake 2 East Haridashi":	"S2e",
	"Sekiwake 2 West Haridashi":	"S2w",
	"Sekiwake 3 East Haridashi":	"S3e",
	"Sekiwake 3 West Haridashi":	"S3w",

	"Komusubi 1 East Haridashi":	"K1e",
	"Komusubi 1 West Haridashi":	"K1w",
	"Komusubi 2 East Haridashi":	"K2e",
	"Komusubi 2 West Haridashi":	"K2w",
	"Komusubi 3 East Haridashi":	"K3e",
	"Komusubi 3 West Haridashi":	"K3w",
}


from collections import defaultdict
all_titles = defaultdict(lambda:"N/A",{
    "Yokozuna 1 East":	"Y1e",
    "Yokozuna 1 East Yokozuna-Ozeki": "Y1e",
	"Yokozuna 1 West":	"Y1w",
	"Yokozuna 1 West Yokozuna-Ozeki": "Y1w",
	"Yokozuna 2 East":	"Y2e",
	"Yokozuna 2 East Yokozuna-Ozeki": "Y2e",
	"Yokozuna 2 West":	"Y2w",
	"Yokozuna 2 West Yokozuna-Ozeki": "Y2w",
	"Yokozuna 3 East":	"Y3e",
	"Yokozuna 3 West":	"Y3w",

	"Ozeki 1 East":	"O1e",
	"Ozeki 1 West":	"O1w",
	"Ozeki 2 East":	"O2e",
	"Ozeki 2 West":	"O2w",
	"Ozeki 3 East":	"O3e",
	"Ozeki 3 West":	"O3w",

	"Sekiwake 1 East":	"S1e",
	"Sekiwake 1 West":	"S1w",
	"Sekiwake 2 East":	"S2e",
	"Sekiwake 2 West":	"S2w",
	"Sekiwake 3 East":	"S3e",
	"Sekiwake 3 West":	"S3w",

	"Komusubi 1 East":	"K1e",
	"Komusubi 1 West":	"K1w",
	"Komusubi 2 East":	"K2e",
	"Komusubi 2 West":	"K2w",
	"Komusubi 3 East":	"K3e",
	"Komusubi 3 West":	"K3w",

	# Haridashi (overflow) mapping
	"Yokozuna 1 East Haridashi":	"Y1e",
	"Yokozuna 1 West Haridashi":	"Y1w",
	"Yokozuna 2 East Haridashi":	"Y2e",
	"Yokozuna 2 West Haridashi":	"Y2w",
	"Yokozuna 3 East Haridashi":	"Y3e",
	"Yokozuna 3 West Haridashi":	"Y3w",

	"Ozeki 1 East Haridashi":	"O1e",
	"Ozeki 1 West Haridashi":	"O1w",
	"Ozeki 2 East Haridashi":	"O2e",
	"Ozeki 2 West Haridashi":	"O2w",
	"Ozeki 3 East Haridashi":	"O3e",
	"Ozeki 3 West Haridashi":	"O3w",

	"Sekiwake 1 East Haridashi":	"S1e",
	"Sekiwake 1 West Haridashi":	"S1w",
	"Sekiwake 2 East Haridashi":	"S2e",
	"Sekiwake 2 West Haridashi":	"S2w",
	"Sekiwake 3 East Haridashi":	"S3e",
	"Sekiwake 3 West Haridashi":	"S3w",

	"Komusubi 1 East Haridashi":	"K1e",
	"Komusubi 1 West Haridashi":	"K1w",
	"Komusubi 2 East Haridashi":	"K2e",
	"Komusubi 2 West Haridashi":	"K2w",
	"Komusubi 3 East Haridashi":	"K3e",
	"Komusubi 3 West Haridashi":	"K3w",
	"Maegashira 1 East": "M1e",
	"Maegashira 1 West": "M1w",
	"Maegashira 2 East": "M2e",
	"Maegashira 2 West": "M2w",
	"Maegashira 3 East": "M3e",
	"Maegashira 3 West": "M3w",
	"Maegashira 4 East": "M4e",
	"Maegashira 4 West": "M4w",
	"Maegashira 5 East": "M5e",
	"Maegashira 5 West": "M5w",
	"Maegashira 6 East": "M6e",
	"Maegashira 6 West": "M6w",
	"Maegashira 7 East": "M7e",
	"Maegashira 7 West": "M7w",
	"Maegashira 8 East": "M8e",
	"Maegashira 8 West": "M8w",
	"Maegashira 9 East": "M9e",
	"Maegashira 9 West": "M9w",
	"Maegashira 10 East": "M10e",
	"Maegashira 10 West": "M10w",
	"Maegashira 11 East": "M11e",
	"Maegashira 11 West": "M11w",
	"Maegashira 12 East": "M12e",
	"Maegashira 12 West": "M12w",
	"Maegashira 13 East": "M13e",
	"Maegashira 13 West": "M13w",
	"Maegashira 14 East": "M14e",
	"Maegashira 14 West": "M14w",
	"Maegashira 15 East": "M15e",
	"Maegashira 15 West": "M15w",
	"Maegashira 16 East": "M16e",
	"Maegashira 16 West": "M16w",
	"Maegashira 17 East": "M17e",
	"Maegashira 17 West": "M17w",
	"Maegashira 18 East": "M18e",
	"Maegashira 18 West": "M18w",
	"Juryo 1 East":	"J1e",
    "Juryo 1 West":	"J1w",
    "Juryo 2 East":	"J2e",
    "Juryo 2 West":	"J2w",
    "Juryo 3 East":	"J3e",
    "Juryo 3 West":	"J3w",
    "Juryo 4 East":	"J4e",
    "Juryo 4 West":	"J4w",
    "Juryo 5 East":	"J5e",
    "Juryo 5 West":	"J5w",
    "Juryo 6 East":	"J6e",
    "Juryo 6 West":	"J6w",
    "Juryo 7 East":	"J7e",
    "Juryo 7 West":	"J7w",
    "Juryo 8 East":	"J8e",
    "Juryo 8 West":	"J8w",
    "Juryo 9 East":	"J9e",
    "Juryo 9 West":	"J9w",
    "Juryo 10 East":	"J10e",
    "Juryo 10 West":	"J10w",
    "Juryo 11 East":	"J11e",
    "Juryo 11 West":	"J11w",
    "Juryo 12 East":	"J12e",
    "Juryo 12 West":	"J12w",
    "Juryo 13 East":	"J13e",
    "Juryo 13 West":	"J13w",
    "Juryo 14 East":	"J14e",
    "Juryo 14 West":	"J14w",
})
rank_weights = defaultdict(lambda: 1, {
	'y1': 3.79,
	'y2': 3.79,
	'y3': 3.79,
	'o1': 2.2896,
	'o2': 2.2896,
	'o3': 2.2896,
	's1': 1.5961,
	's2': 1.5961,
	's3': 1.5961,
	'k1': 1.2755,
	'k2': 1.2755,
	'k3': 1.2755,
	'm1': 1.1274,
	'm2': 1.0589,
	'm3': 1.0272,
	'm4': 1.0126,
	'm5': 1.0058,
	'm6': 1.0027,
	'm7': 1.0012,
	'm8': 1.0006,
	'm9': 1.0003,
	'm10': 1.0001,
	'm11': 1.0001,
})

rank_weights_linear = defaultdict(lambda: 1, {
	'y1': 2.7869,
	'y2': 2.7869,
	'y3': 2.7869,
	'o1': 2.5808,
	'o2': 2.5808,
	'o3': 2.5808,
	's1': 2.3746,
	's2': 2.3746,
	'k1': 2.2371,
	'k2': 2.2371,
	'm1': 2.0997,
	'm2': 2.0309,
	'm3': 1.9622,
	'm4': 1.8935,
	'm5': 1.8247,
	'm6': 1.756,
	'm7': 1.6873,
	'm8': 1.6186,
	'm9': 1.5498,
	'm10': 1.4811,
	'm11': 1.4124,
	'm12': 1.3436,
	'm13': 1.2749,
	'm14': 1.2062,
	'm15': 1.1375,
	'm16': 1.0687,
	'm17': 1.0,
	'm18': 1.0,
	'j1': 0.9313,
	'j2': 0.8625,
	'j3': 0.7938,
	'j4': 0.7251,
	'j5': 0.6564,
	'j6': 0.5876,
	'j7': 0.5189,
	'j8': 0.4502,
	'j9': 0.3814,
	'j10': 0.3127,
	'j11': 0.244,
	'j12': 0.1753,
	'j13': 0.1065,
	'j14': 0.0378,
})
# CSV export function
def export_rikishi_to_csv(rikishi_list, filename="rikishi_results.csv"):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Write CSV header
        writer.writerow([
            "Name", "Wins", "Losses", "Record",
            "Neustadl", "Weighted Neustadl", "Rank",
            "Inverse Rank", "Weight", "Sanyaku", "Starting Rank", "Beats",
        ])

        # Write Rikishi data line-by-line
        for rikishi in rikishi_list:
            # try:
            # print(
            #     rikishi.name,
            #     rikishi.wins,
            #     rikishi.losses,
            #     rikishi.record,
            #     rikishi.neustadl,
            #     rikishi.weighted_neustadl if rikishi.weighted_neustadl is not None else "",
            #     rikishi.rank if rikishi.rank is not None else "",
            #     rikishi.inverse_rank if rikishi.inverse_rank is not None else "",
            #     rikishi.weight if rikishi.weight is not None else "",
            #     rikishi.sanyaku,
            #     rikishi.starting_rank,
            #     rikishi.beats,  # Joins opponents by semicolon
            #
            # )
            writer.writerow([
                rikishi.name,
                rikishi.wins,
                rikishi.losses,
                rikishi.record,
                rikishi.neustadl,
                rikishi.weighted_neustadl if rikishi.weighted_neustadl is not None else "",
                rikishi.rank if rikishi.rank is not None else "",
                rikishi.inverse_rank if rikishi.inverse_rank is not None else "",
                rikishi.weight if rikishi.weight is not None else "",
                rikishi.sanyaku,
                rikishi.starting_rank,
                ";".join([rikishi_obj.name for rikishi_obj in rikishi.beats]),  # Joins opponents by semicolon
            ])
            # except Exception as e:
            #     print("Got an error writing", e)

def import_rikishi_from_csv(filename="rikishi_results.csv"):
    rikishi_list = []
    with open(filename, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            name = row["Name"]
            beats = row["Beats"].split(';') if row["Beats"] else []
            rikishi = Rikishi(name, beats)
            rikishi.record = int(row["Record"])
            # rikishi.neustadl = row["Neustadl"]
            rikishi.wins = int(row["Wins"])
            rikishi.losses = int(row["Losses"])
            rikishi.weighted_neustadl = float(row["Weighted Neustadl"]) if row["Weighted Neustadl"] else None
            rikishi.rank = int(row["Rank"])
            rikishi.inverse_rank = int(row["Inverse Rank"])
            rikishi.weight = float(row["Weight"]) if row["Weight"] else None
            # print(rikishi.weight)
            rikishi.sanyaku = row["Sanyaku"]
            rikishi.starting_rank = row["Starting Rank"]
            # print(row)
            # print(rikishi.beats)
            rikishi_list.append(rikishi)
    return rikishi_list

def fill_in_rikishi_list_data(rikishi_list, use_linear_weights=False):
    # create a dictionary to map names to Rikishi objects for quick lookup
    rikishi_dict = {rikishi.name: rikishi for rikishi in rikishi_list}
    # print(rikishi_dict)
    for rikishi in rikishi_list:
        rikishi.beats = [rikishi_dict[opponent] for opponent in rikishi.beats if opponent in rikishi_dict]
        rikishi.inverse_rank = len(rikishi_list)-rikishi.rank-1
        #figure out rank weight
        rikishi.weight = rank_weights[rikishi.starting_rank[:-1].lower()] if use_linear_weights==False else rank_weights_linear[rikishi.starting_rank[:-1].lower()]


    #handle simple neustadl calcs, and add
    for rikishi in rikishi_list:
        # print(rikishi.name , "#####")
        for opponent in rikishi.beats:
            rikishi.neustadl += opponent.wins
            # print(rikishi.name)
            rikishi.weighted_raw_record += opponent.weight
            # print(rikishi.weighted_raw_record)

        #base score is all the weights of opponents you beat
        rikishi.weighted_neustadl = rikishi.weighted_raw_record

    #assign weighted records to all rikishi
    for rikishi in rikishi_list:
        for opponent in rikishi.beats:
            # print(rikishi.name, opponent.name)
            #final score is all the weights of opponents you beat, and the weights of all the opponents
            #your opponent beat
            rikishi.weighted_neustadl += opponent.weighted_raw_record

        # print(rikishi.name, rikishi.weighted_neustadl)

    return rikishi_list

prestandard_codes = ['195709', '195711']

changed_names = {
    "Haguroyama" : "Annenyama",
    "Daikirin" : 'Kirinji',
    'Hokutoumi': "Hoshi",
    "Takanohana": "Takahanada",
    "Wakanohana": "Wakahanada",
    "Harumafuji" : "Ama",
    "Kirishima" : "Kiribayama",
    "Kotozakura": "Kotonowaka",
}

basho_months = ["01", "03", "05", "07", "09", "11"]


def get_prev_basho(year, month, base_dir="../bashoresultsv2"):
    months = [int(m) for m in basho_months]
    idx = months.index(int(month))
    while True:
        if idx == 0:
            year -= 1
            idx = len(months) - 1
        else:
            idx -= 1
        prev_month = months[idx]
        prev_basho_code = f"{year}{prev_month:02d}"
        csv_path = os.path.join(base_dir, f"{prev_basho_code}.csv")
        if os.path.isfile(csv_path):
            return year, f"{prev_month:02d}"

import statistics
import numpy as np
def print_stats(title, data):
    print(f"{title}:")
    print(f"    {'Lowest val:':<20}{min(data):<10} {'Highest val:':<15}{max(data):<10}")
    print(f"    {'Median:':<20}{statistics.median(data):<10.2f}")
    print(f"    {'Mean:':<20}{statistics.mean(data):<10.2f}")
    print(f"    {'Q1:':<20}{np.percentile(data, 25):<10.2f} {'Q3:':<15}{np.percentile(data, 75):<10.2f}")



with open("intai_wrestlers.csv", newline='', encoding="utf-8") as f:
	reader = csv.DictReader(f)
	intai_wrestlers = list(reader)
all_tourneys = []
used_basho_codes = []
for year in range(1958, 2026):
# for year in range(1995, 1996):
    for month in basho_months:
        if year > 2025 or (year == 2025 and int(month) > 7):
            break
        basho_code = f"{year}{month}"
        csv_name = f"../bashoresultsv2/{basho_code}.csv"

        if not os.path.isfile(csv_name):
            continue
        with open(csv_name, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        # find previous eligible basho (skip cancelled basho files)
        prev = get_prev_basho(year, month)
        if not prev or not all(prev):
            print(f"No previous basho for {basho_code}")
            continue
        prev_year, prev_month = prev
        prev_basho_code = f"{prev_year}{prev_month}"
        prev_csv_name = f"../bashoresultsv2/{prev_basho_code}.csv"

        with open(prev_csv_name, newline='', encoding='utf-8') as f:
            prev_rows = list(csv.DictReader(f))

        sanyaku_num = 0
        for row in rows:
            if row["Sanyaku"]:
                sanyaku_num += 1
            else:
                break #sanyaku should be ordered, so we should be able to short circuit here

        old_sanyaku_num = 0
        for prow in prev_rows:
            if prow["Sanyaku"]:
                old_sanyaku_num += 1
            else:
                break #sanyaku should be ordered, so we should be able to short circuit here

        sanyaku_adj = old_sanyaku_num-sanyaku_num
        # rik.rank-sanyaku_adj) #oldrank adj
        # truerank = rik.rank - rik.record
        # adjusted_tr = truerank - sanyaku_adj
        # signed diff = adjusted_tr - new_rank
        #
        # print("#################")
        # print(prev_basho_code, "banzuke to ", basho_code)
        sd_tourney = []
        for row in rows:
            #skip sanyaku and juryo
            if "M" not in row["Starting Rank"]:
                continue
            name = row["Name"]

            shouldbreak = False
            for irow in intai_wrestlers:
                if basho_code == irow["File"] and name in irow["Name"]:
                    shouldbreak = True
                    # print("found intai")
                    break
            if shouldbreak: continue

            # found = False
            for prow in prev_rows:
                if name in changed_names and prow["Name"] == changed_names[name]:
                    print("found change")
                    time.sleep(1)

                if name == prow["Name"] or (name in changed_names and prow["Name"] == changed_names[name]):
                    found = True

                    #take only juryo
                    if "J" not in prow["Starting Rank"]:
                        break

                    newrank = int(row["Rank"])
                    oldrank = int(prow["Rank"])
                    truerank = oldrank - int(prow["Record"])
                    adjusted_tr = truerank - sanyaku_adj
                    signed_diff = adjusted_tr - newrank

                    # if signed_diff >= 15:
                    #     print(prev_basho_code, name, prow["Wins"], oldrank-sanyaku_adj, newrank, adjusted_tr, signed_diff, prow["Starting Rank"], row["Starting Rank"])
                    #     print("found!")
                    #     time.sleep(1)
                    sd_tourney.append(signed_diff)
                    # print(name, prow["Wins"], oldrank-sanyaku_adj, newrank, adjusted_tr, signed_diff)
                    break


        # print(f"Total for {prev_basho_code} banzuke to {basho_code}: {sd_tourney_sum}")
        print(prev_basho_code + " to " + basho_code, sum(sd_tourney), sd_tourney)
        if sd_tourney:
            all_tourneys.append(sd_tourney)
        used_basho_codes.append(f"{prev_basho_code} to {basho_code}")

print_stats("Real Basho Sum of all Signed Diffs", [sum(n) for n in all_tourneys])

print_stats("Real Basho Sum of all Signed Diffs (Absolute Values) ", [sum([abs(x) for x in n]) for n in all_tourneys])


all_tourney_stats = []

for i, values in enumerate(all_tourneys):
	stats = {
		"min": min(values),
		"max": max(values),
		"mean": statistics.mean(values),
		"median": statistics.median(values),
		"q1": np.percentile(values, 25),
		"q3": np.percentile(values, 75),
	}
	all_tourney_stats.append(stats)

# collect lists of each stat across all tournaments
stat_keys = ["min", "max", "mean", "median", "q1", "q3"]
all_stats_by_type = {k: [stats[k] for stats in all_tourney_stats] for k in stat_keys}

# Now print stats of stats:
print("Stats of Each Stat Across All Tournaments")

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










