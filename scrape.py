import requests
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
            print(
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
                rikishi.beats,  # Joins opponents by semicolon

            )
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

        # if not "Makuuchi" in table.get_text():
        #     break
        if "Sandanme" in table.get_text():
            # makuuchi_table = table
            break
    #
    # if makuuchi_table is None:
    #     print("Makuuchi Banzuke table not found.")
    #     exit()rikishi.inverse_rank/len(rikishi_list)

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
                        # if row.find("td", class_="emptycell"):
                        #     #handle weird old banzuke edge cases
                        #     searcher = row.find("td", class_="shikona")
                        #     if searcher == None:
                        #         searcher = row.find("td", class_="debut")
                        #         if searcher == None:
                        #             searcher = row.find("td", class_="retired")
                        #             if searcher == None:
                        #                 searcher = row.find("td", class_="promotion")
                        #     searched_idx = cells.index(searcher)
                        #     if searched_idx > 1:
                        #         name = cells[2].find("a").get_text(strip=True)
                        #         result_cell = cells[3]
                        #     else:
                        #         name = cells[1].find("a").get_text(strip=True)
                        #         result_cell = cells[0]
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
def sort_non_ozeki_raw(rlist, rating_options):
    global global_hack_var
    global_hack_var = len(rlist) - 5
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
def prevent_down_or_equal_rank_with_kk(sorted_rikishi, offset):
    #offset is the index offset from the first rank to the first index of the list we are given
    #basically, its the amount of previous sanyaku, so we can figure out where someones actual rank position is even after we've pruned the sorted_rikishi list
    final_ranking = sorted_rikishi.copy()

    while True:
        any_detected = False
        for i, rikishi in enumerate(final_ranking.copy()):

            if rikishi.wins >= 8 and offset+i >= rikishi.rank:
                any_detected = True
                print("detected spurious dowmrank", rikishi.name, rikishi.wins, rikishi.rank, i, offset+i)
                current_pos = offset+i
                while current_pos >= rikishi.rank:
                    actual_pos = current_pos-offset
                    print('rank=', rikishi.rank, 'curr_pos', current_pos, 'finish_pos', current_pos+1, 'actual_pos', actual_pos)
                    swap_index = actual_pos-1
                    if swap_index <0:
                        break #we reached the top of the list

                    final_ranking[actual_pos], final_ranking[swap_index] = (
                        final_ranking[swap_index],
                        final_ranking[actual_pos],
                    )

                    current_pos -= 1

        if not any_detected:
            break

    for i, rikishi in enumerate(final_ranking):
        if rikishi.wins >= 8 and offset+i >= rikishi.rank:
            print("!!!!")
            print("detected still low", rikishi.name, rikishi.wins, rikishi.rank, i)
            time.sleep(1)

    return final_ranking

#ensure that someone does not go up in rank on a makekoshi
#note this is only performed on komusubi and below, so there is never, for example, ozeki getting "promoted" because another ozeki moved to yokozuna
def prevent_uprank_with_mk(sorted_rikishi, offset):
    #offset is the index offset from the first rank to the first index of the list we are given
    #basically, the amount of previous sanyaku, so we can figure out where someones actual rank position is even after we've pruned the sorted_rikishi list
    final_ranking = sorted_rikishi.copy()

    while True:
        any_detected = False
        for i, rikishi in enumerate(final_ranking.copy()):
            # Only proceed if rikishi had at least 8 wins
            if rikishi.wins < 8 and offset+i < rikishi.rank:
                any_detected = True
                print("detected spurious uprank", rikishi.name, rikishi.wins, rikishi.rank, i, offset+i)

                current_pos = offset+i
                while current_pos < rikishi.rank:
                    actual_pos = current_pos-offset
                    print('rank=', rikishi.rank, 'curr_pos', current_pos, 'finish_pos', current_pos+1, 'actual_pos', actual_pos)
                    swap_index = actual_pos+1
                    if swap_index > len(sorted_rikishi)-1:
                        break #we reached the top of the list

                    final_ranking[actual_pos], final_ranking[swap_index] = (
                        final_ranking[swap_index],
                        final_ranking[actual_pos],
                    )

                    current_pos += 1

        if not any_detected:
            break

    for i, rikishi in enumerate(final_ranking):
        if rikishi.wins < 8 and offset+i < rikishi.rank:
            print("!!!!")
            print("detected still high", rikishi.name, rikishi.wins, rikishi.rank, i, offset+i)
            time.sleep(1)

    return final_ranking

rank_list_print = [f"M{i}{side}" for i in range(1, 19) for side in ("e", "w")] + [f"J{i}{side}" for i in range(1, 15) for side in ("e", "w")]

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

def write_ranks(writer, printing_list, sanyaku_num):
    writer.writerow([
            "Name", "Old Rank Title", "New Rank Title", '"True Rank" Title', "Old Rank", "New Rank","True Rank", "Wins", "Signed Diff", "Weighted Neustadl", "Sanyaku Defeated Score Raw","Sanyaku Defeated Score Weighted",
        ])
    for i in range(0, len(printing_list)):
        rik = printing_list[i]
        row = []

        row.append(rik.name)
        row.append(rik.starting_rank)
        row.append(rik.new_rank_title)
        truerank = len(printing_list) - (rik.inverse_rank + rik.record)
        row.append(rank_list_print[truerank-sanyaku_num] if truerank-sanyaku_num >= 0 and truerank-sanyaku_num < len(rank_list_print) else "N/A" )
        row.append(rik.rank) #previous rank
        row.append(i) #new rank
        row.append(truerank)
        row.append(rik.wins)
        row.append(truerank-i)
        row.append(rik.weighted_neustadl)


        raw_score = 0
        weighted_score = 0
        for beatr in rik.beats:
            if beatr.sanyaku:
                raw_score += 1
                weighted_score += rank_weights[beatr.sanyaku.lower()[:2]]
        row.append(raw_score)
        row.append(weighted_score)
        print(row)
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

#sanyaku heuristics:
#0 = no heuristics, will not attempt to determine sekiwakes etc
#1 = fair, simple heuristics
#2 = prevent downranking
#ranking system:
#0 = Truerank strict, regular neustadl
#1 = Truerank strict, weighted neustadl
#2 = Truerank fuzzy, regular Neustadl
#3 = Truerank fuzzy, weighted  neustadl
def make_banzuke(rikishi_list,filename, use_sanyaku_heuristics=1, ranking_options=0):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        yokozuna_list = []
        ozeki_list = []
        komusubi_list = []
        sekiwake_list = []

        #make lambda print
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


        #first, handle yokozuna and ozeki, which are simply based on who has the best record
        #TODO prio1 make this change with use_sanyaku_heuristics
        #TODO handle ties in record
        yokozuna_sorted = sorted(yokozuna_list, key=lambda x: x.record, reverse=True)
        ozeki_sorted = sorted(ozeki_list, key=lambda x: x.record, reverse=True)

        assign_rank_titles(yokozuna_sorted, "Y")
        assign_rank_titles(ozeki_sorted, "O")

#
        #create and update the final banzuke list
        final_rlist = yokozuna_sorted + ozeki_sorted


        #TODO handle ozeki promotion/demotion criteria

        sorted_list = sort_non_ozeki_raw(rikishi_list, ranking_options)

        final_sekiwake_out = []
        final_komusubi_out = []
        #do heuristics to determine who gets the sekiwake slots
        # print("pop " , sorted_list.pop(0).name)
        if use_sanyaku_heuristics > 0:
            for rikishi in sorted_list[:]:
                #first, if someone was already a sekiwake, and posted a kachikoshi, they are a sekiwake
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
                while(len(final_sekiwake_out) < 2):
                    final_sekiwake_out.append(sorted_list.pop(0))


            #now, sort the sekiwake rankings
            #if we are in fair mode, simply assign them based on true rank
            #if we are using more unfair heuristics, apply them instead


            #now, sort the sekiwake ranking based on true rank
            final_sekiwake_out = sort_non_ozeki_raw(final_sekiwake_out, ranking_options)
            if use_sanyaku_heuristics == 2:
                offset = len(yokozuna_list) + len(ozeki_list)
                # final_sekiwake_out = prevent_downrank_with_kk(final_sekiwake_out, offset)
                # final_sekiwake_out = prevent_uprank_with_mk(final_sekiwake_out, offset)

            assign_rank_titles(final_sekiwake_out, "S")
            final_rlist += final_sekiwake_out


            #TODO: make non-heuristic out for sekiwake (doable with just changing the final sorted list out)


            #Next, figure out who our komusubi are

            for rikishi in sorted_list[:]:
                #first, check if there are any komusubi remaining with a kachikoshi. They are still komusubi
                if rikishi in komusubi_list and rikishi.record > 0:
                    final_komusubi_out.append(rikishi)
                    sorted_list.remove(rikishi)
                    continue

            sorted_list = prevent_down_or_equal_rank_with_kk(sorted_list, len(yokozuna_list) + len(ozeki_list) + len(final_sekiwake_out))
            previous_ranks_offset = len(yokozuna_list) + len(ozeki_list) + len(final_sekiwake_out) + len(final_komusubi_out)
            #the threshold for making it to komusubi no matter what. This is the
            komusubi_threshold = len(sorted_list) + len(final_sekiwake_out) + 2

            #If we don't have enough komusubi after checking for existing komusubi, and people who under normal circumstances would made it to komusubi even with 2 slots filled,
            #Then fill the slots with the next highest sorted wrestler.
            while len(final_komusubi_out) < 2 and sorted_list:
                final_komusubi_out.append(sorted_list.pop(0))

            #for every individual who WOULD have made it past the threshold for a SEKIWAKE with their true rank, and isn't already a komusubi, simply put them in as new slots
            for rikishi in sorted_list[:]:
                truerank = rikishi.inverse_rank+rikishi.record

                if truerank > komusubi_threshold:
                    print(truerank, rikishi.name, rikishi.record)
                    # print(rikishi.name, truerank)
                    final_komusubi_out.append(rikishi)
                    sorted_list.remove(rikishi)

            #finally, if someone is m1e, and posted a kachikoshi, make them a komusubi
            for rikishi in sorted_list[:]:
                if rikishi.starting_rank == "M1e" and rikishi.wins >= 8:
                    # print("found")
                    final_komusubi_out.append(rikishi)
                    sorted_list.remove(rikishi)
                    break

            #sort our komusubi appropriately by our ranking algorithm
            final_komusubi_out = sort_non_ozeki_raw(final_komusubi_out, ranking_options)


            assign_rank_titles(final_komusubi_out, "K")
            final_rlist += final_komusubi_out



        #now, finally handle maegashira
        offset = len(yokozuna_list) + len(ozeki_list) + len(final_sekiwake_out) + len(final_komusubi_out)

        #handle spurious upranks on makekoshi, remove
        sorted_list = prevent_uprank_with_mk(sorted_list, offset)

        sanyaku_num = len(final_rlist)
        assign_maegashira_juryo(sorted_list, sanyaku_num)

        final_rlist += sorted_list
        # for r in final_rlist:
        #     print(r.name, r.new_rank_title)
        write_ranks(writer, final_rlist, sanyaku_num)



# basho_months = ["01", "03", "05", "07", "09", "11"]
# for year in range(1970, 2026):
#     for month in basho_months:
#         if year == 1964 and month in ["01",]:
#         #     print("skipping 01 03 05 2014")
#             continue
#         if year > 2025 or (year == 2025 and int(month) > 5):
#             break
#         basho_code = f"{year}{month}"
#         csv_name = f"bashoresultsv2/{basho_code}.csv"
#         scrape_sumodb(f'Banzuke.aspx?b={basho_code}', csv_name)
#
#

# "Banzuke.aspx?b=202503"
# scrape_sumodb('Banzuke.aspx?b=202305', "bashoresults/202305.csv")
rlist = fill_in_rikishi_list_data(import_rikishi_from_csv("bashoresults/201701.csv"))
#


make_banzuke(rlist, "testoutnewsystem.csv", 2, 1)
# #

# make_banzuke(rlist, "fairbanzukeoutput/202305banzuke.csv", 2, 1)

# import os
#
# input_folder = "bashoresults"
# output_folder = "fairbanzukeoutput"
#
# os.makedirs(output_folder, exist_ok=True)
#
# for fname in os.listdir(input_folder):
# 	if not fname.endswith(".csv"):
# 		continue
# 	basho_code = fname[:-4]  # removes '.csv'
# 	in_path = os.path.join(input_folder, fname)
# 	out_path = os.path.join(output_folder, f"{basho_code}banzuke.csv")
#
# 	rlist = fill_in_rikishi_list_data(import_rikishi_from_csv(in_path))
# 	make_banzuke(rlist, out_path, 2, 1)
#

# rlist = fill_in_rikishi_list_data(import_rikishi_from_csv("Natsu2025weights.csv"))
# make_banzuke(rlist, "testoutnatsunormal.csv", 2, 0)
# rlist = fill_in_rikishi_list_data(import_rikishi_from_csv("Natsu2025weights.csv"))
# make_banzuke(rlist, "testoutnatsuweightedfuzzy.csv", 2, 3)
# rlist = fill_in_rikishi_list_data(import_rikishi_from_csv("Natsu2025weights.csv"))
# make_banzuke(rlist, "testoutnatsuweighted.csv", 2, 1)
#
# rlistlinear = fill_in_rikishi_list_data(import_rikishi_from_csv("Natsu2025weights.csv"), True)
#
# make_banzuke(rlistlinear, "testoutnatsuweightlinear.csv", 2, True)
#
#
