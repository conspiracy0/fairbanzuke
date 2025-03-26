import requests
from bs4 import BeautifulSoup
import time
import csv
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

import csv

# CSV export function
def export_rikishi_to_csv(filename="rikishi_results.csv"):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Write CSV header
        writer.writerow([
            "Name", "Wins", "Losses", "Record",
            "Neustadl", "Weighted Neustadl", "Rank",
            "Inverse Rank", "Weight", "Sanyaku", "Beats",
        ])

        # Write Rikishi data line-by-line
        for rikishi in rikishi_list:
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
                 ";".join(rikishi.beats),  # Joins opponents by semicolon
            ])

BASE_URL = "https://sumodb.sumogames.de/"
TARGET_URL = f"{BASE_URL}Banzuke.aspx?b=202503"

# Get the main page
response = requests.get(TARGET_URL)
soup = BeautifulSoup(response.content, "html.parser")

# Locate the "Makuuchi Banzuke" table
# tables = soup.find_all("table")
tables = soup.find_all("table", class_="banzuke")

# print(makuuchi_table.get_text())

rikishi_list = []
rank_counter = 1
# sanyakutitles = ["Yokozuna", 'Ozeki', 'Komusubi', 'Sekiwake']
sanyakutitles = {
    "Yokozuna 1 East": "Y1e",
    "Yokozuna 1 West": "Y1w",
    "Ozeki 1 East": "O1e",
    "Ozeki 1 West": "O1w",
    "Ozeki 2 East": "O2e",
    "Ozeki 2 West": "O2w",
    "Ozeki 3 East": "O3e",
    "Ozeki 3 West": "O3w",
    "Sekiwake 1 East": "S1e",
    "Sekiwake 1 West": "S1w",
    "Sekiwake 2 East": "S2e",
    "Sekiwake 2 West": "S2w",
    "Komusubi 1 East": "K1e",
    "Komusubi 1 West": "K1w",
    "Komusubi 2 East": "K2e",
    "Komusubi 2 West": "K2w",
}


for table in tables:

    # if not "Makuuchi" in table.get_text():
    #     break
    if "Sandanme" in table.get_text():
        # makuuchi_table = table
        break
#
# if makuuchi_table is None:
#     print("Makuuchi Banzuke table not found.")
#     exit()

    rows = table.find_all("tr")
    header_cells = [cell.get_text(strip=True) for cell in rows[0].find_all(['th'])]

    # result_index = header_cells.index("Result")
    result_indices = [i for i, cell in enumerate(header_cells) if cell == "Result"]
    # print(result_index)
    # print(header_cells)


    for row in rows[1:]:
        cells = row.find_all("td")
        print("#####row#####")
        for idx in result_indices:
            print("#####idx######")
            print(len(cells))
            if len(cells) > idx:


                # print("cell ", str(idx), ": ", cells[idx])
                if idx == 0:
                    name = cells[1].find("a").get_text(strip=True)
                else:
                    name = cells[3].find("a").get_text(strip=True)
                print(name)
                result_cell = cells[idx]
                link_tag = result_cell.find("a")
                opp_beat = []
                rank = ""
                if link_tag and 'href' in link_tag.attrs:
                    #get beats info
                    url = f"{BASE_URL}{link_tag['href']}"
                    wrestler_page = requests.get(url)
                    # print(url)
                    # print(wrestler_page)
                    # print(cells)
                    wrestler_soup = BeautifulSoup(wrestler_page.content, "html.parser")
                    titlerank = wrestler_soup.find("td", class_="rb_topleft").contents[0]

                    results_table = wrestler_soup.find("table", class_="rb_torikumi")
                    # print(results_table)
                    # print(results_table.get_text())

                    wrestler_rows = results_table.find_all("tr")
                    for wrestler_row in wrestler_rows:
                        wrestler_cells = wrestler_row.find_all("td")
                        # print("#######")
                        # print(wrestler_cells[1])
                        img = wrestler_cells[1].find('img')['src']
                        if "shiro" in img or "fusensho" in img:
                            # print("found won")
                            opp_beat.append(wrestler_cells[3].find("a").get_text(strip=True).split()[1])
                        # if "kuro" in img or "fusenpai" in img:
                        #     print("found loss")

                    rikishi_obj = Rikishi(name, opp_beat)
                    if titlerank in sanyakutitles.keys():
                        rikishi_obj.sanyaku = sanyakutitles[titlerank]
                    rikishi_obj.rank = rank_counter
                    rank_counter += 1
                    rikishi_obj.inverse_rank = 70-rikishi_obj.rank
                    #don't weight makushita wrestlers
                    rikishi_obj.weight = rikishi_obj.inverse_rank/69 if rank_counter <= 70 else 0
                    rikishi_list.append(rikishi_obj)
                    if rank_counter % 10 == 0:
                        print("sleeping to avoid rate timeout")
                        time.sleep(10)

                else:
                    print("failed somehow due to link fucking up")
                    # return
                    # links.append()
                    # print(link_tag['href'].strip())
            print("#####end idx######")
        print("####end row###")

for rikishi in rikishi_list:
    print(rikishi.name, ", ", rikishi.inverse_rank, ", ", rikishi.rank, ", ", rikishi.weight, ", ", rikishi.beats)


export_rikishi_to_csv()

