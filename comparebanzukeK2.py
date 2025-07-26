import os
import csv

def increment_basho_code(basho_code):
	year = int(basho_code[:4])
	month = int(basho_code[4:6])
	basho_months = [1, 3, 5, 7, 9, 11]
	idx = basho_months.index(month)
	if idx == len(basho_months) - 1:
		year += 1
		month = basho_months[0]
	else:
		month = basho_months[idx + 1]
	return f"{year}{month:02d}"

custom_dir = "fairbanzukeoutput"
actual_dir = "bashoresultsv2"




def find_incongruous(search_str):
    # results = []
    count = 0
    for fname in os.listdir(custom_dir):
        if not fname.endswith("banzuke.csv"):
            continue
        basho_code = fname[:6]
        next_code = increment_basho_code(basho_code)
        custom_path = os.path.join(custom_dir, fname)
        actual_path = os.path.join(actual_dir, f"{next_code}.csv")

        if not os.path.isfile(actual_path):
            print(f"Missing actual banzuke file: {actual_path}")
            continue

        with open(custom_path, newline='', encoding='utf-8') as f:
            custom_reader = csv.DictReader(f)
            # for row in custom_reader:
            #     print(row)
            #     print(row["New Rank Title"])
            custom_search_ranks = [(row["Name"], row["New Rank Title"]) for row in custom_reader if search_str in row.get("New Rank Title")]
            # print(custom_search_ranks)

        with open(actual_path, newline='', encoding='utf-8') as f:
            actual_reader = csv.DictReader(f)
            actual_starting_ranks = [(row["Name"], row["Starting Rank"]) for row in actual_reader if "Starting Rank" in row]
            # print(actual_starting_ranks)


        for custom_rank in custom_search_ranks:
            # if custom_rank not in actual_starting_ranks:
            for actual_rank in actual_starting_ranks:
                if actual_rank[0] == custom_rank[0] and actual_rank[1][:2] != custom_rank[1][:2]:
                    # results.append((fname, k2_rank))
                    print(f"For {fname}, Our banzuke: {custom_rank}, and at {next_code}, real banzuke: {actual_rank}")
                    # print(f"For {fname}, Our banzuke: {custom_rank}, and at {next_code}, real banzuke: {next((tup for tup in actual_starting_ranks if tup[0] == custom_rank[0]), None)}")
                    count += 1

    print(count)

    # for fname, k2_rank in results:
    #     print(f"In {fname}, K2 rank not found in actual: {k2_rank}")
    #     print(len(results))

# find_incongruous("K2")
# find_incongruous("K3")
# find_incongruous("K4")
find_incongruous("S2")
find_incongruous("S3")
find_incongruous("S4")
