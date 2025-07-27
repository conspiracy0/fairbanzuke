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

#used to get data from previous basho for ozeki promotion criteria
def import_single_rikishi_from_csv(target_name, filename="rikishi_results.csv"):
    rikishi_list = []
    with open(filename, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        alt_name = changed_names.get(target_name)
        for row in reader:
            if row["Name"] == target_name or (alt_name and row["Name"] == alt_name):
                name = target_name
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
                return rikishi

    print("!!! didn't find previous guy", target_name, "in ", filename)
    time.sleep(4)

def scrape_sumodb(suffix, csvname):
    BASE_URL = "https://sumodb.sumogames.de/"
    TARGET_URL = f"{BASE_URL}{suffix}"

    # Get the main page
    response = requests.get(TARGET_URL)
    soup = BeautifulSoup(response.content, "html.parser")


    # Locate the "Makuuchi Banzuke" table
    # tables = soup.find_all("table")
    tables = soup.find_all("table", class_="banzuke")

    rikishi_list = []
    rank_counter = 0


    for table in tables:


        if "Sandanme" in table.get_text():
            # makuuchi_table = table
            break

        rows = table.find_all("tr")
        header_cells = [cell.get_text(strip=True) for cell in rows[0].find_all(['th'])]

        # result_index = header_cells.index("Result")
        result_indices = [i for i, cell in enumerate(header_cells) if cell == "Result"]
        # print(result_index)
        # print(header_cells)


        for row in rows[1:]:
            # last_short_rank = ""
            while True:
                try:
                    cells = row.find_all("td")
                    print("#####row#####")
                    # print(result_indices)
                    # print(cells)
                    print(row.find("td", class_="shikona"))
                    # print(cells[0].get_text())
                    # print("cell print", row.find_all("td", class_="emptycell"))
                    for idx in result_indices:
                        print("#####idx######")
                        print


                        #attempt short circuit
                        short_rank = row.find("td", class_="short_rank").get_text()
                        print("short_rank", short_rank)
                        gigabreak = False
                        if "Ms" in short_rank or "OB" in short_rank or "TD" in short_rank:
                            for rikishi in rikishi_list:
                                if name in rikishi.beats:
                                    print("Found")
                                    break
                            gigabreak = True
                        if gigabreak:
                            print("gigabreaking")
                            break

                        result_cell = None
                        if row.find("td", class_="emptycell"):
                            # handle weird old banzuke edge cases
                            searcher = None
                            for cls in ["shikona", "debut", "retired", "promotion"]:
                                searcher = row.find("td", class_=cls)
                                if searcher is not None:
                                    break
                            if searcher is not None:
                                searched_idx = cells.index(searcher)
                                if searched_idx > 1:
                                    name = cells[2].find("a").get_text(strip=True)
                                    result_cell = cells[3]
                                else:
                                    name = cells[1].find("a").get_text(strip=True)
                                    result_cell = cells[0]
                        else:
                            result_cell = cells[idx]
                            # print("cell ", str(idx), ": ", cells[idx])
                            if idx == 0:
                                #fix break if there is no east side
                                if cells[1].find("a" )== None:
                                    continue
                                name = cells[1].find("a").get_text(strip=True)
                            else:
                                name = cells[3].find("a").get_text(strip=True)

                        print("name=", name)





                        link_tag = result_cell.find("a")
                        opp_beat = []
                        rank = ""
                        if link_tag and 'href' in link_tag.attrs:
                            #get beats info
                            url = f"{BASE_URL}{link_tag['href']}"
                            wrestler_page = requests.get(url)
                            wrestler_soup = BeautifulSoup(wrestler_page.content, "html.parser")
                            titlerank = wrestler_soup.find("td", class_="rb_topleft").contents[0]

                            results_table = wrestler_soup.find("table", class_="rb_torikumi")

                            wrestler_rows = results_table.find_all("tr")
                            for wrestler_row in wrestler_rows:
                                wrestler_cells = wrestler_row.find_all("td")

                                img = wrestler_cells[1].find('img')['src']
                                if "shiro" in img or "fusensho" in img:
                                    opp_beat.append(wrestler_cells[3].find("a").get_text(strip=True).split()[1])

                            rikishi_obj = Rikishi(name, opp_beat)

                            print(rikishi_obj.beats)
                            print( ";".join([rikishi for rikishi in rikishi_obj.beats]))

                            if titlerank in sanyakutitles.keys():
                                rikishi_obj.sanyaku = sanyakutitles[titlerank]
                            #todo fix yokozuna-ozeki thing

                            rikishi_obj.starting_rank = all_titles[titlerank]
                            print("startingrank =", rikishi_obj.starting_rank)
                            print(rank_weights[rikishi_obj.starting_rank[:-1].lower()])
                            rikishi_obj.rank = rank_counter
                            rank_counter += 1

                            rikishi_list.append(rikishi_obj)
                            if rank_counter % 10 == 0:
                                print("sleeping to avoid rate timeout")
                                time.sleep(4)
                                # rikishi_list = fill_in_rikishi_list_data(rikishi_list)
                                # export_rikishi_to_csv(rikishi_list, csvname)
                                # return
                            if row.find("td", class_="emptycell"):
                                break
                        else:
                            print("failed somehow due to link fucking up")

                        print("#####end idx######")
                    break
                except (AttributeError, TypeError, ConnectionError) as e:
                    print("sleeping on normal fetch section", e)
                    time.sleep(1)


    rikishi_list = fill_in_rikishi_list_data(rikishi_list)
    for rikishi in rikishi_list:
        print(rikishi.name, ", ", rikishi.inverse_rank, ", ", rikishi.rank, ", ", rikishi.weight, ", ", rikishi.beats, rikishi.starting_rank, rikishi.weight)

    export_rikishi_to_csv(rikishi_list, csvname)


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

def simple_neustadl_banzuke(rikishi_list):
    return sorted(rikishi_list, key=lambda rikishi: rikishi.neustadl, reverse=True)


def weighted_neustadl_banzuke(rikishi_list):
    return sorted(rikishi_list, key=lambda rikishi: rikishi.weighted_neustadl, reverse=True)

sekiwake_vals = ['S1e', 'S1w', 'S2e', 'S2w']
def sort_non_ozeki_raw_compare(a, b):

    #true rank is the "true placement" they should be at given their rank and record. i.e, a M8e with a 8-7 should go to M7e
    atruerank = (a.inverse_rank + a.record)
    btruerank = (b.inverse_rank + b.record)

    #first, if one wrestlers true rank is objectively better than another wrestler, then he should go higher.
    if atruerank > btruerank:
        return (-1)
    if atruerank < btruerank:
        return 1

    #if there are multiple people at the same true rank, then break ties with the weighted neustadl
    # the neustadl score is the sum of the weighted ranks you beat, and every weighted rank your opponents beat.
    # this means that if you beat better opponents, who either did better in the tournament, and/or were higher ranked, you will do better
    # if (a.weighted_neustadl > b.weighted_neustadl):
    #     return (-1)
    # elif (a.weighted_neustadl < b.weighted_neustadl):
    #     return 1
    if (a.neustadl > b.neustadl):
        return (-1)
    elif (a.neustadl < b.neustadl):
        return 1


    # final tiebreak, f b is in a.beats, then a should go before b
    if b in a.beats:
        return -1
    elif a in b.beats:
        # if a is in b.beats, then b should go before a
        return 1
    print("returning 0 on ", a.name, "vs", b.name)
    return 0

def sort_non_ozeki_weighted(a, b):
    #true rank is the "true placement" they should be at given their rank and record. i.e, a M8e with a 8-7 should go to M7e
    atruerank = (a.inverse_rank + a.record)
    btruerank = (b.inverse_rank + b.record)

    #first, if one wrestlers true rank is objectively better than another wrestler, then he should go higher.
    if atruerank > btruerank:
        return (-1)
    if atruerank < btruerank:
        return 1

    #if there are multiple people at the same true rank, then break ties with the weighted neustadl
    # the neustadl score is the sum of the weighted ranks you beat, and every weighted rank your opponents beat.
    # this means that if you beat better opponents, who either did better in the tournament, and/or were higher ranked, you will do better
    # if (a.weighted_neustadl > b.weighted_neustadl):
    #     return (-1)
    # elif (a.weighted_neustadl < b.weighted_neustadl):
    #     return 1
    if (a.weighted_neustadl > b.weighted_neustadl):
        return (-1)
    elif (a.weighted_neustadl < b.weighted_neustadl):
        return 1

    # final tiebreak, f b is in a.beats, then a should go before b
    if b in a.beats:
        return -1
    elif a in b.beats:
        # if a is in b.beats, then b should go before a
        return 1
    print("returning 0 on ", a.name, "vs", b.name)
    return 0

rank_list_print = [f"M{i}{side}" for i in range(1, 19) for side in ("e", "w")] + [f"J{i}{side}" for i in range(1, 15) for side in ("e", "w")]

def sort_non_ozeki_weighted_fuzzy(a, b):

    #true rank is the "true placement" they should be at given their rank and record. i.e, a M8e with a 8-7 should go to M7e
    atruerank = (a.inverse_rank + a.record)
    btruerank = (b.inverse_rank + b.record)
    # print("ghv2", global_hack_var)
    atr2 = global_hack_var - atruerank
    btr2 = global_hack_var - btruerank
    atrfindable = atr2 > -1 and atr2 < len(rank_list_print)
    btrfindable = btr2 > -1 and btr2 < len(rank_list_print)
    if atrfindable and btrfindable and (a.name == "Kusano" or b.name == "Kusano") :
        print(a.name, atr2, rank_list_print[atr2], b.name, btr2, rank_list_print[btr2])

    #if a wrestler is more than 2 ranks higher than someone, just automatically place him
    if atruerank - btruerank >= 2:
        print("moving up", a.name, "moving down", b.name, "on raw truerank")
        return (-1)
    if btruerank - atruerank >= 2:
        print("moving up", b.name, "moving down", a.name, "on raw truerank")
        return 1

    #if there are multiple people at the same true rank, then break ties with the weighted neustadl
    # the neustadl score is the sum of the weighted ranks you beat, and every weighted rank your opponents beat.
    # this means that if you beat better opponents, who either did better in the tournament, and/or were higher ranked, you will do better


    if atrfindable and btrfindable:
        # print(a.name, atr2, rank_list_print[atr2], b.name, btr2, rank_list_print[btr2])
        #if they are the same maegashira ranks, try to fuzzy it a bit
        if rank_list_print[atr2][:-1] == rank_list_print[btr2][:-1]:
            # print(a.name, atr2, rank_list_print[atr2], b.name, btr2, rank_list_print[btr2])
            if (a.weighted_neustadl > b.weighted_neustadl):
                print("moving up", a.name, "moving down", b.name, "on fuzzy wn")
                return (-1)
            elif (a.weighted_neustadl < b.weighted_neustadl):
                print("moving up", b.name, "moving down", a.name, "on fuzzy wn")
                return 1

    #if we can't figure it out still, go back to default un-fuzzy behavior
    if atruerank > btruerank:
        return (-1)
    if atruerank < btruerank:
        return 1

    if (a.weighted_neustadl > b.weighted_neustadl):
        print("moving up", a.name, "moving down", b.name, "on leftover wn ")
        return (-1)
    elif (a.weighted_neustadl < b.weighted_neustadl):
        print("moving up", b.name, "moving down", a.name, "on leftover wn ")
        return 1


    # final tiebreak, f b is in a.beats, then a should go before b
    print("got to tiebreaks")
    if b in a.beats:
        return -1
    elif a in b.beats:
        # if a is in b.beats, then b should go before a
        return 1
    print("returning 0 on ", a.name, "vs", b.name)
    return 0

def sort_non_ozeki_fuzzy(a, b):

    #true rank is the "true placement" they should be at given their rank and record. i.e, a M8e with a 8-7 should go to M7e
    atruerank = (a.inverse_rank + a.record)
    btruerank = (b.inverse_rank + b.record)

    #first, if one wrestlers true rank is objectively better than another wrestler, then he should go higher.
    if atruerank - btruerank >= 2:
        return (-1)
    if btruerank - atruerank >= 2:
        return 1

    #if there are multiple people at the same true rank, then break ties with the weighted neustadl
    # the neustadl score is the sum of the weighted ranks you beat, and every weighted rank your opponents beat.
    # this means that if you beat better opponents, who either did better in the tournament, and/or were higher ranked, you will do better
    # if (a.weighted_neustadl > b.weighted_neustadl):
    #     return (-1)
    # elif (a.weighted_neustadl < b.weighted_neustadl):
    #     return 1
    if (a.neustadl > b.neustadl):
        return (-1)
    elif (a.neustadl < b.neustadl):
        return 1


    # final tiebreak, f b is in a.beats, then a should go before b
    if b in a.beats:
        return -1
    elif a in b.beats:
        # if a is in b.beats, then b should go before a
        return 1
    print("returning 0 on ", a.name, "vs", b.name)
    return 0

global_hack_var = None
def sort_non_ozeki_raw(rlist, rating_options, ghackvar = None):
    global global_hack_var
    global_hack_var = len(rlist) - 5 if ghackvar == None else ghackvar
    match rating_options:
        case 0:
            return sorted(rlist, key=cmp_to_key(sort_non_ozeki_raw_compare))
        case 1:
            return sorted(rlist, key=cmp_to_key(sort_non_ozeki_weighted))
        case 2:
            return sorted(rlist, key=cmp_to_key(sort_non_ozeki_fuzzy))
        case 3:
            return sorted(rlist, key=cmp_to_key(sort_non_ozeki_weighted_fuzzy))


#ensure the rikishi is promoted if the rikishi has a kk after raw weighted neustadl evaluation
#note this will only be done during evaluation for komusubi and below, so it should never break on sekiwake being capped at sekiwake
def prevent_down_or_equal_rank_with_kk(sorted_rikishi, offset, sanyaku_adj):
    #offset is the index offset from the first rank to the first index of the list we are given
    #basically, its the amount of previous sanyaku, so we can figure out where someones actual rank position is even after we've pruned the sorted_rikishi list
    final_ranking = sorted_rikishi.copy()

    while True:
        any_detected = False
        iteratelist = final_ranking.copy()
        # print(f"sanyaku_adj: {sanyaku_adj}, list_len: {len(iteratelist)}, ")
        for i, rikishi in enumerate(iteratelist):

            adj_rank = rikishi.rank - sanyaku_adj

            # if rikishi.wins >= 8 and offset+i >= rikishi.rank + removal_offset:
            if rikishi.wins >= 8 and offset+i >= adj_rank:
                any_detected = True
                print("detected spurious downrank", rikishi.name, rikishi.wins, rikishi.rank, i, offset+i)

                current_pos = offset+i
                while current_pos >= adj_rank:

                    actual_pos = current_pos-offset
                    print('rank=', rikishi.rank, 'curr_pos', current_pos, 'finish_pos', current_pos-1, 'actual_pos', actual_pos)

                    swap_index = actual_pos-1
                    if swap_index <0:
                        print("!!! HIT SWAP_INDEX CEILING")
                        break #we reached the top of the list


                    final_ranking[actual_pos], final_ranking[swap_index] = (
                        final_ranking[swap_index],
                        final_ranking[actual_pos],
                    )

                    current_pos -= 1

        if not any_detected:
            break

    for i, rikishi in enumerate(final_ranking):

        if rikishi.wins >= 8 and offset+i >= rikishi.rank - sanyaku_adj:
            print("!!!!")
            print("detected still low(spurious downrank)", rikishi.name, rikishi.wins, rikishi.rank, i+offset)
            time.sleep(10)

    return final_ranking


#ensure that someone does not go up in rank on a makekoshi
#note this is only performed on komusubi and below, so there is never, for example, ozeki getting "promoted" because another ozeki moved to yokozuna
def prevent_uprank_with_mk(sorted_rikishi, offset, sanyaku_adj):
    #offset is the index offset from the first rank to the first index of the list we are given
    #basically, the amount of previous sanyaku, so we can figure out where someones actual rank position is even after we've pruned the sorted_rikishi list
    final_ranking = sorted_rikishi.copy()
    failure_list = []
    # for i, rikishi in enumerate(final_ranking.copy()):
    #     print(i, rikishi.name)
    while True:
        any_detected = False
        for i, rikishi in enumerate(final_ranking.copy()):
            if rikishi.wins < 8:

                #if we have rikishi so bad they go below the end of the list and can't be bubbled, put them in a separate list to deal with later
                if (rikishi.inverse_rank + rikishi.record) < 0:
                    print("removing failure", rikishi.name)
                    failure_list.append(rikishi)
                    final_ranking.remove(rikishi)
                    continue

                adj_rank = rikishi.rank - sanyaku_adj
                #otherwise, if they are higher than their starting rank on a makekoshi, trigger a bubble
                # if offset+i < rikishi.rank:
                if offset+i < adj_rank:
                    any_detected = True
                    print("detected spurious uprank", rikishi.name, rikishi.wins, i, offset+i, adj_rank, rikishi.rank, sanyaku_adj)

                    current_pos = offset+i
                    while current_pos < adj_rank:
                        actual_pos = current_pos-offset
                        print('rank=', rikishi.rank, 'curr_pos', current_pos, 'finish_pos', current_pos+1, 'actual_pos', actual_pos)
                        swap_index = actual_pos+1
                        if swap_index > len(final_ranking)-1:
                            #if we have rikishi so bad they go below the end of the list and can't be bubbled, put them in a separate list to deal with later
                            print("removing failure at swap", rikishi.name)
                            failure_list.append(rikishi)
                            final_ranking.remove(rikishi)
                            break #we reached the top of the list

                        final_ranking[actual_pos], final_ranking[swap_index] = (
                            final_ranking[swap_index],
                            final_ranking[actual_pos],
                        )

                        current_pos += 1
        if not any_detected:
            break


    #handle the people going down to makushita
    failure_list = sorted(failure_list, key=cmp_to_key(sort_non_ozeki_raw_compare))
    final_ranking += failure_list
    for i, rikishi in enumerate(final_ranking):
        # if rikishi.wins < 8 and offset+i < rikishi.rank and rikishi not in failure_list:
        if rikishi.wins < 8 and offset+i < rikishi.rank - sanyaku_adj and rikishi not in failure_list:
            print("!!!!")
            print("detected still high(spurious uprank)", rikishi.name, rikishi.wins, rikishi.rank, i, offset+i)
            time.sleep(5)

    return final_ranking



def print_row(row, east, west, rlistlen, should_print_wn=False, is_maegashira_offset = 0):

    #if we are going to try and print the actual rank name on the true rank
    if is_maegashira_offset > 0:
        trueranke = rlistlen - (east.inverse_rank + east.record)
        # if trueranke - is_maegashira_offset -1 > -1:\
        if trueranke- is_maegashira_offset > -1 and trueranke - is_maegashira_offset < len(rank_list_print):
            # print(len(rank_list_print), trueranke - is_maegashira_offset, east.name, east.record)
            trueranke = rank_list_print[trueranke - is_maegashira_offset]

    else:
        trueranke = rlistlen - (east.inverse_rank + east.record)


    if west:
        if is_maegashira_offset > 0:
            truerankw = rlistlen - (west.inverse_rank + west.record)
            if truerankw- is_maegashira_offset > -1 and truerankw - is_maegashira_offset < len(rank_list_print):
            # print(len(rank_list_print), trueranke - is_maegashira_offset, east.name, east.record)
                truerankw = rank_list_print[truerankw - is_maegashira_offset]
        else:
            truerankw = rlistlen - (west.inverse_rank + west.record)

        if should_print_wn:
            print(
                f"{row[1]}: {row[0]} (N:{east.neustadl}) (WN:{east.weighted_neustadl}) (TrueRank:{trueranke}) | "
                f"{row[3]}: {row[2]} (N:{west.neustadl}) (WN:{west.weighted_neustadl}) (TrueRank:{truerankw})"
            )
        else:
            print(
                f"{row[1]}: {row[0]} (N:{east.neustadl}) (TrueRank:{trueranke}) | "
                f"{row[3]}: {row[2]} (N:{west.neustadl}) (TrueRank:{truerankw})"
            )
    else:
        if should_print_wn:
             print(
                f"{row[1]}: {row[0]} (N:{east.neustadl}) (WN:{east.weighted_neustadl}) (TrueRank:{trueranke}) | "
                f"{row[3]}: (empty)"
            )
        else:
            print(
                f"{row[1]}: {row[0]} (N:{east.neustadl}) (TrueRank:{trueranke}) | "
                f"{row[3]}: (empty)"
            )

def write_ranks(writer, printing_list, old_sanyaku_num, sanyaku_num, rank_list_print):
    writer.writerow([
            "Name", "Old Rank Title", "New Rank Title", '"True Rank" Title', "Old Rank","Old Rank Adj","New Rank","True Rank", "Wins", "Signed Diff", "Weighted Neustadl", "Sanyaku Defeated Score Raw","Sanyaku Defeated Score Weighted",
        ])

    # print(, old_sanyaku_num, sanyaku_num)
    sanyaku_diff = old_sanyaku_num-sanyaku_num
    # print(rank_list_print)
    for i in range(0, len(printing_list)):
        rik = printing_list[i]
        row = []

        row.append(rik.name)
        row.append(rik.starting_rank)
        row.append(rik.new_rank_title)

        truerank = rik.rank - rik.record

        # adjusted_tr = truerank-old_sanyaku_num

        sanyaku_adj = old_sanyaku_num-sanyaku_num
        oldrank_adj = rik.rank-sanyaku_adj
        adjusted_tr = truerank - sanyaku_adj
        # adjusted_i = i+sanyaku_adj
        # print(sanyaku_adj, "sa")
        rank_print = adjusted_tr-sanyaku_num
        # print(rank_print, rik.name, rank_list_print[rank_print] )
        row.append(rank_list_print[rank_print] if rank_print >= 0 and rank_print < len(rank_list_print) else "N/A" )
        row.append(rik.rank) #previous rank
        row.append(rik.rank-sanyaku_adj) #oldrank adj
        row.append(i) #new rank
        row.append(adjusted_tr)
        row.append(rik.wins)
        row.append(adjusted_tr-i)
        row.append(rik.weighted_neustadl)


        raw_score = 0
        weighted_score = 0
        for beatr in rik.beats:
            if beatr.sanyaku:
                raw_score += 1
                weighted_score += rank_weights[beatr.sanyaku.lower()[:2]]
        row.append(raw_score)
        row.append(weighted_score)
        # print(truerank-sanyaku_num, row)
        writer.writerow(row)


def assign_rank_titles(rikishi_sorted, abbrev):
	for idx, rikishi in enumerate(rikishi_sorted):
		# even index: east, odd index: west
		slot = idx // 2 + 1
		side = 'e' if idx % 2 == 0 else 'w'
		rikishi.new_rank_title = f"{abbrev}{slot}{side}"

def assign_maegashira_juryo(maegashira_and_juryo, sanyaku_num):
	# number of maegashira: 42 - sanyaku_num
	maegashira_slots = 42 - sanyaku_num
	# first maegashira_slots*2 are maegashira, rest are juryo
	for idx, rikishi in enumerate(maegashira_and_juryo):
		if idx < maegashira_slots:
			slot = idx // 2 + 1
			side = 'e' if idx % 2 == 0 else 'w'
			rikishi.new_rank_title = f"M{slot}{side}"
		else:
			juryo_idx = idx - maegashira_slots
			slot = juryo_idx // 2 + 1
			side = 'e' if juryo_idx % 2 == 0 else 'w'
			rikishi.new_rank_title = f"J{slot}{side}"


def get_prev_bashos(basho_code, folder):
    basho_months = ["01", "03", "05", "07", "09", "11"]
    year = int(basho_code[:4])
    month = basho_code[4:]

    idx = basho_months.index(month)
    prev_bashos = []
    lookback_idx = idx - 1
    lookback_year = year

    while len(prev_bashos) < 2:
        if lookback_idx < 0:
            lookback_year -= 1
            lookback_idx = len(basho_months) - 1
        prev_code = f"{lookback_year}{basho_months[lookback_idx]}"
        csv_path = os.path.join(folder, f"{prev_code}.csv")
        if os.path.isfile(csv_path):
            prev_bashos.append(prev_code)
        lookback_idx -= 1
        if lookback_year < 1957:
            break
    return prev_bashos

#
# heuristics:
# All:
#
#     Will track and handle Ozeki promotion(33 wins, based on average promotion wins of 33.32) and demotion, and repromotion from kadoban (10 wins)
#     Will handle the opening of additional sekiwake and komusubi slots
#     Will always promote M1e to Komusubi at all times
#     Will not demote komusubi or Sekiwake with a kachikoshi FROM the ranks, but they can be downranked inside the rank.
#
# 0:
#     For all non-sanyaku wrestlers, will rank wrestlers simply on performance. Wrestlers with better performances than other wrestlers, with a makekoshi, can be promoted on a losing record, and wrestlers with worse performances can be demoted on a kachikoshi
#
# 1:
#     For all non-sanyaku wrestlers, prevent downranking or staying at the same rank if you scored a kachikoshi, and prevent going up on a makekoshi
#     TODO Newly promoted wrestlers will start lower than others (check this is real)
#
#ranking system:
#0 = Truerank strict, regular neustadl
#1 = Truerank strict, weighted neustadl
#2 = Truerank fuzzy, regular Neustadl
#3 = Truerank fuzzy, weighted  neustadl
def make_banzuke(rikishi_list,filename, bcode, bfolder, heuristic_set=1, ranking_options=0):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        print("BASHO: ", bcode)
        writer = csv.writer(file)

        yokozuna_list = []
        ozeki_list = []
        komusubi_list = []
        sekiwake_list = []

        final_sekiwake_out = []
        final_komusubi_out = []
        rlistlen = len(rikishi_list)

        for rikishi in rikishi_list[:]:  # Iterate over a shallow copy
            if rikishi.sanyaku in ['O1e', 'O1w', 'O2e', 'O2w', 'O3e', 'O3w']:
                ozeki_list.append(rikishi)
                rikishi_list.remove(rikishi)
            elif rikishi.sanyaku in ['S1e', 'S1w', 'S2e', 'S2w', "S3w", "S3e"]:
                sekiwake_list.append(rikishi)
                # rikishi_list.remove(rikishi)
            elif rikishi.sanyaku in ['Y1e', 'Y1w', "Y2e", "Y2w"]:
                yokozuna_list.append(rikishi)

                rikishi_list.remove(rikishi)
            elif rikishi.sanyaku in ['K1e', 'K1w', 'K2e', 'K2w']:
                komusubi_list.append(rikishi)
                # rikishi_list.remove(rikishi)

        old_ozeki_len = len(ozeki_list)
        old_yokozuna_len = len(yokozuna_list)
        old_sekiwake_len = len(sekiwake_list)
        old_komusubi_len = len(komusubi_list)
        old_sanyaku_num = old_ozeki_len + old_komusubi_len + old_sekiwake_len + old_yokozuna_len
        #first, handle yokozuna and ozeki, which are simply based on who has the best record
        #TODO prio1 make this change with heuristic_set

        yokozuna_sorted = sorted(yokozuna_list, key=lambda x: x.record, reverse=True)
        assign_rank_titles(yokozuna_sorted, "Y")
        #create and update the final banzuke list
        final_rlist = yokozuna_sorted


        #handle ozeki promotion check
        prevcodes = get_prev_bashos(bcode, bfolder)

        for rikishi in sekiwake_list[:]:
            cum_wins = rikishi.wins
            gigabreak = False
            for i, code in enumerate(prevcodes):

                bashostring = bfolder+"/"+code+".csv"
                prev_result = import_single_rikishi_from_csv(rikishi.name, bashostring)
                cum_wins += prev_result.wins
                if i == 0:
                    #if the previous tournament, this person was ozeki, and they get ten wins, return them to ozeki
                    if "O" in prev_result.sanyaku and rikishi.wins >= 10:
                        ozeki_list.append(rikishi)
                        rikishi_list.remove(rikishi)
                        sekiwake_list.remove(rikishi)
                        gigabreak = True
                        break
                if gigabreak:
                    break

            #if the sekiwake has had at least 33 wins over the last 3 basho, he is now an ozeki
            #33.32 wins is the average number of wins for promotion to ozeki on an ozeki run, so that is the basis.
            if cum_wins > 33:
                ozeki_list.append(rikishi)
                rikishi_list.remove(rikishi)
                sekiwake_list.remove(rikishi)

        #handle ozeki demotion
        demoted_ozeki = []
        for rikishi in ozeki_list[:]:
            bashostring = bfolder+"/"+prevcodes[0]+".csv"
            prev_result = import_single_rikishi_from_csv(rikishi.name, bashostring)
            if prev_result.wins < 8 and rikishi.wins < 8:
                ozeki_list.remove(rikishi)
                #failing kadoban ozeki will ALWAYS go to sekiwake.
                demoted_ozeki.append(rikishi)
                # rikishi_list.remove(rikishi)

        ozeki_sorted = sorted(ozeki_list, key=lambda x: x.record, reverse=True)
        assign_rank_titles(ozeki_sorted, "O")
        final_rlist += ozeki_sorted


        #create and handle the tentative pick list of the remaining wrestlers
        sorted_list = sort_non_ozeki_raw(rikishi_list, ranking_options)


        for rikishi in sorted_list[:]:
            #first, if someone was already a sekiwake, and posted a kachikoshi, they are still a sekiwake
            if rikishi in sekiwake_list and rikishi.record > 0:
                final_sekiwake_out.append(rikishi)
                sorted_list.remove(rikishi)
                continue

            #if a komusubi gets at least 11 wins, move him to sekiwake
            if rikishi in komusubi_list and rikishi.wins >= 11:
                final_sekiwake_out.append(rikishi)
                komusubi_list.remove(rikishi)
                sorted_list.remove(rikishi)
                continue


        #if there are 2 sekiwake now, hooray, we are done
        #if not, we figure out who is doing the best in terms of their true rank (true rank = rank + wins) (this will always be the first person(s) on the sorted list remaining), then add them to the sekiwake list
        if len(final_sekiwake_out) < 2:
            sthresh = old_sanyaku_num-old_komusubi_len-old_sekiwake_len
            print(sthresh, "sthresh")
            while(len(final_sekiwake_out) < 2):
                if heuristic_set >= 1:
                    #if we are not doing raw ranks, we have to find the first eligible rikishi and use them
                    for i, obj in enumerate(sorted_list):
                        if (obj.sanyaku and (obj.wins > 7 or obj.rank <= sthresh+len(final_sekiwake_out))) or obj.wins > 7:
                            print(obj.name, obj.rank, i, sthresh+len(final_sekiwake_out))
                            final_sekiwake_out.append(obj)
                            del sorted_list[i]
                            break
                else:
                    final_sekiwake_out.append(sorted_list.pop(0))


        #now, add the demoted ozeki
        final_sekiwake_out += demoted_ozeki
        #now, sort the sekiwake rankings
        #if we are in fair mode, simply assign them based on true rank
        #if we are using more unfair heuristics, apply them instead


        #now, sort the sekiwake ranking based on true rank
        final_sekiwake_out = sort_non_ozeki_raw(final_sekiwake_out, ranking_options)

        # print([r.name for r in final_sekiwake_out])
        # print(old_sanyaku_num)
        #assign and append titles to sekiwake list
        assign_rank_titles(final_sekiwake_out, "S")
        final_rlist += final_sekiwake_out


        #next, figure out who our komusubi are


        # the threshold for making it to komusubi no matter what. This is the amount of sanyaku
        komusubi_threshold = old_sanyaku_num-old_komusubi_len-komusubi_force_offset

        #If we don't have enough komusubi after checking for existing komusubi
        #Then fill the slots with the next highest sorted wrestler.
        # print(old_sanyaku_num-old_komusubi_len, len(final_komusubi_out))
        while len(final_komusubi_out) < 2 and sorted_list:
            if heuristic_set >= 1:
                #if we are not doing raw ranks, we have to find the first eligible komusubi, and use them
                for i, obj in enumerate(sorted_list):
                    if (obj.sanyaku and (obj.wins > 7 or obj.rank <= old_sanyaku_num-old_komusubi_len+len(final_komusubi_out))) or obj.wins > 7:
                        print(obj.name, obj.rank, i, old_sanyaku_num-old_komusubi_len+len(final_komusubi_out))
                        final_komusubi_out.append(obj)
                        del sorted_list[i]
                        break
            else:
                final_komusubi_out.append(sorted_list.pop(0))

        #handle forced promotions to komusubi, even with no slots available
        for rikishi in sorted_list[:]:
            #check if there are any komusubi remaining with a kachikoshi. They are still
            #notably, this only triggers if they weren't already selected in the ranked choice earlier
            if rikishi in komusubi_list and rikishi.record > 0:
                final_komusubi_out.append(rikishi)
                sorted_list.remove(rikishi)
                continue

            #if someone is m1e, and posted a kachikoshi, make them a komusubi, even if no other slots. This is the current reigning heuristic.
            if rikishi.starting_rank == "M1e" and rikishi.wins >= 8:
                final_komusubi_out.append(rikishi)
                sorted_list.remove(rikishi)
                continue

            # #if a sekiwake has exactly 7 wins, it doesn't make sense to downrank them below komusubi. So don't.
            # if "S" in rikishi.starting_rank and rikishi.wins == 7:
            #     final_komusubi_out.append(rikishi)
            #     sorted_list.remove(rikishi)
            #     continue

            #for every individual who WOULD have made it past the threshold for a Komusubi+an offset with their true rank, and isn't already a komusubi, put them in as new slots
            truerank = rikishi.rank-rikishi.record

            if truerank < komusubi_threshold:
                print("!!!!!!!!!!hit over komusubi threshold", truerank, rikishi.name, rikishi.record)
                komusubi_threshold_list.append(f"In {bcode}, {rikishi.name} was put to Komusubi.")
                final_komusubi_out.append(rikishi)
                sorted_list.remove(rikishi)
                continue


        assign_rank_titles(final_komusubi_out, "K")
        final_rlist += final_komusubi_out



        #if we have heuristic set 1, then we prevent spurious down/upranks in the remaining maegashira
        if heuristic_set >= 1:

            #this number is the difference between the number of sanyaku without komusubi in the output banzuke, vs the prev banzuke
            upper_san_diff = old_sanyaku_num- len(final_rlist)

            prev_rank_offset = old_sanyaku_num - upper_san_diff
            # old_sanyaku_num-old_komusubi_len-len(final_rlist)
            sorted_list = prevent_down_or_equal_rank_with_kk(sorted_list, prev_rank_offset, upper_san_diff)
            sorted_list = prevent_uprank_with_mk(sorted_list, prev_rank_offset, upper_san_diff)


        #now, finally handle maegashira

        sanyaku_num = len(final_rlist)
        maegashira_slots = 42 - sanyaku_num

        rank_list_print = []
        for i in range(1, math.ceil(maegashira_slots / 2) + 1):
            for side in ("e", "w"):
                if len(rank_list_print) < maegashira_slots:
                    rank_list_print.append(f"M{i}{side}")

        # add juryo ranks as before
        rank_list_print += [f"J{i}{side}" for i in range(1, 15) for side in ("e", "w")]
        # for n in rank_list_print:
        #     print(n)
        assign_maegashira_juryo(sorted_list, sanyaku_num)

        final_rlist += sorted_list
        # for r in final_rlist:
        #     print(r.name, r.new_rank_title)
        write_ranks(writer, final_rlist, old_sanyaku_num, sanyaku_num, rank_list_print)




# basho_months = ["01", "03", "05", "07", "09", "11"]
# for year in range(1957, 2026):
#     for month in basho_months:
#         if year == 2012 and month in ["01","03", "07",]:
#         #     print("skipping 01 03 05 2014")
#             continue
#         if year > 2025 or (year == 2025 and int(month) > 5):
#             break
#         basho_code = f"{year}{month}"
#         csv_name = f"bashoresultsv2/{basho_code}.csv"
#         scrape_sumodb(f'Banzuke.aspx?b={basho_code}', csv_name)
#

#included only for ozeki tracking on the first two bashos
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
# for basho_code in prestandard_codes:
# 	csv_name = f"bashoresultsv2/{basho_code}.csv"
# 	scrape_sumodb(f'Banzuke.aspx?b={basho_code}', csv_name)
# # #

# "Banzuke.aspx?b=202503"
# scrape_sumodb('Banzuke.aspx?b=202305', "bashoresults/202305.csv")

komusubi_force_offset = 2
komusubi_threshold_list = []
# banzukecode = "200803"
# banzukecode ="197111"
banzukecode = "198403"
bashofolder = "bashoresultsv2"
rlist = fill_in_rikishi_list_data(import_rikishi_from_csv(bashofolder+"/"+banzukecode+".csv"))
make_banzuke(rlist, "testoutnewsystem.csv",banzukecode, bashofolder, 2, 1 )
# # # # # #

# make_banzuke(rlist, "fairbanzukeoutput/202305banzuke.csv", 2, 1)

# import os

input_folder = "bashoresultsv2"
# output_folder = "fairbanzukeoutputnofixes"
output_folder = "fairbanzukeoutput"
os.makedirs(output_folder, exist_ok=True)

for fname in os.listdir(input_folder):
    if not fname.endswith(".csv"):
        continue
    basho_code = fname[:-4]  # removes '.csv'
    if basho_code in prestandard_codes:
        continue
    in_path = os.path.join(input_folder, fname)
    out_path = os.path.join(output_folder, f"{basho_code}banzuke.csv")

    rlist = fill_in_rikishi_list_data(import_rikishi_from_csv(in_path))
    make_banzuke(rlist, out_path, basho_code, input_folder, 2, 1)
#
for n in komusubi_threshold_list:
    print(n)

print(len(komusubi_threshold_list))


##### fix playoff wins

# input_folder = "bashoresultsv2"
# input_folder = "editedbashosv2"
# output_folder =
# os.makedirs(output_folder, exist_ok=True)

# with open("validators/playofffix.csv", newline='', encoding='utf-8') as f:
#     reader = csv.DictReader(f)
#     fixrows = list(reader)
#     fixfieldnames = reader.fieldnames
#
#     for row in fixrows:
#         bcode = row["Date"]
#         in_path = os.path.join(input_folder, bcode+".csv")
#         print(in_path)
#         # out_path = os.path.join(output_folder, fname)
#         with open(in_path, newline='', encoding='utf-8') as f2:
#             bashoreader = csv.DictReader(f2)
#             bashorows = list(bashoreader)
#             bashofieldnames = bashoreader.fieldnames
#             # print(bashofieldnames)
#         for brow in bashorows:
#             # print(brow["Name"], row["Winner"])
#             if brow["Name"] == row["Winner"]:
#                 print("Before: ", brow["Name"], brow["Beats"])
#                 brow["Beats"] = brow["Beats"].split(';')
#                 brow["Beats"].remove(row["Loser"])
#                 brow["Beats"] = ";".join(brow["Beats"])
#                 # print(brow["Name"], brow["Beats"])
#                 brow["Wins"] = int(brow["Wins"])-1
#                 brow["Record"] = brow['Wins'] * 2
#                 brow["Losses"] = 15 - brow['Wins']
#
#         # Write the updated rows to the output folder
#         with open(in_path, "w", newline='', encoding='utf-8') as fout:
#             writer = csv.DictWriter(fout, fieldnames=bashofieldnames)
#             writer.writeheader()
#             writer.writerows(bashorows)
#
#         rlist = fill_in_rikishi_list_data(import_rikishi_from_csv(in_path))
#         export_rikishi_to_csv(rlist, in_path)
