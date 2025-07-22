import requests
from bs4 import BeautifulSoup
import csv, time, json

from requests.exceptions import ConnectionError

intlist = list(range(16))
sumourlbase = "https://sumodb.sumogames.de/"

sanyaku_dict = {
    "Y1e": "y", "Y1w": "y",
    "Y2e": "y", "Y2w": "y",
    "Y3e": "y", "Y3w": "y",
    "O1e": "o", "O1w": "o",
    "O2e": "o", "O2w": "o",
    "O3e": "o", "O3w": "o",
    "S1e": "s", "S1w": "s",
    "S2e": "s", "S2w": "s",
    "S3e": "s", "S3w": "s",
    "K1e": "k", "K1w": "k",
    "K2e": "k", "K2w": "k",
    "K3e": "k", "K3w": "k",
}

def scrape_rank_change(rank_start, rank_end, ignore_absences=0):
    """
    Returns a list of 16 dicts, one per possible win–loss split (0–15 to 15–0).
    Each dict has: "wins", "total_matches", "sanyaku_results" (list of per-wrestler dicts).
    """
    results = []

    for i in range(8):
        losses = i
        wins = intlist[-(i + 1)]
        url = (
            f"https://sumodb.sumogames.de/Query.aspx?show_form=0"
            f"&rowcount=5&form1_rank={rank_start}&form1_wins={wins}&form1_losses={losses}"
            f"&form1_year=1958-now&form2_rank={rank_end}"
        )
        reverseurl = (
            f"https://sumodb.sumogames.de/Query.aspx?show_form=0"
            f"&rowcount=5&form1_rank={rank_start}&form1_wins={losses}&form1_losses={wins}"
            f"&form1_year=1958-now&form2_rank={rank_end}"
        )

        # Retry loop until parsing succeeds
        while True:
            try:
                response = requests.get(url)
                lresponse = requests.get(reverseurl)

                soup = BeautifulSoup(response.content, "html.parser")
                lsoup = BeautifulSoup(lresponse.content, "html.parser")

                results_text = soup.find(string=lambda text: "results found" in text)
                lresults_text = lsoup.find(string=lambda text: "results found" in text)

                amount = int(results_text.strip().split(" ")[0])
                lamount = int(lresults_text.strip().split(" ")[0])

                sanyaku_resultsw = []
                sanyaku_resultsl = []

                if amount != 0:
                    table = soup.find("table", class_="record")
                    if table:
                        sanyaku_resultsw = get_sanyaku_results(table, sumourlbase)

                if lamount != 0:
                    ltable = lsoup.find("table", class_="record")
                    if ltable:
                        sanyaku_resultsl = get_sanyaku_results(ltable, sumourlbase)

                break  # parsed without exception

            except (AttributeError, TypeError, ConnectionError) as e:
                print("sleeping on normal fetch section", e)
                time.sleep(10)

        print(i, intlist[-(i + 1)], amount, lamount)
        results.append({
            "wins": wins,
            "total_matches": amount,
            "sanyaku_results": sanyaku_resultsw
        })
        results.append({
            "wins": losses,
            "total_matches": lamount,
            "sanyaku_results": sanyaku_resultsl
        })

        time.sleep(0.5)

    results.sort(key=lambda x: x["wins"])
    print(f"finished {rank_start} → {rank_end}")
    return results




def get_sanyaku_results(table, base_url):
    """
    From a <table class="record">, follow each wrestler’s detail link (cell[3]),
    parse <table class="rb_torikumi"> on their detail page, count black-star wins
    vs. sanyaku ranks, and return a list of dicts [{"y":…, "o":…, "s":…, "k":…}, …].
    """
    sanyaku_results = []
    rows = table.find_all("tr")[2:]  # skip header rows

    for row in rows:
        cells = row.find_all("td")
        record = cells[3]
        link = record.find("a")

        sanyaku_wins = {"y": 0, "o": 0, "s": 0, "k": 0}

        if link and link.has_attr("href"):
            indlink = base_url + link["href"]

            while True:
                try:
                    indresp = requests.get(indlink)
                    indsoup = BeautifulSoup(indresp.content, "html.parser")
                    indtable = indsoup.find("table", class_="rb_torikumi")

                    if not indtable:
                        print("something fucked up on the manual results page, throwing error and retrying")
                        raise TypeError("something fucked up")

                    for irow in indtable.find_all("tr"):
                        icells = irow.find_all("td")
                        if len(icells) < 4:
                            continue
                        img = icells[1].find("img")
                        if img and img.get("src") == "img/hoshi_shiro.gif":
                            ctext = icells[3].get_text()
                            for key, val in sanyaku_dict.items():
                                if key in ctext:
                                    sanyaku_wins[val] += 1

                    break  # parsed without exception

                except (AttributeError, TypeError, ConnectionError) as e:
                    print("sleeping on sanyaku section", e)
                    time.sleep(10)

        sanyaku_results.append(sanyaku_wins)
        time.sleep(0.5)

    return sanyaku_results


all_ranks = (
    [f"s{i}{side}" for i in range(1, 4) for side in ["e", "w"]] +
    [f"k{i}{side}" for i in range(1, 4) for side in ["e", "w"]] +
    [f"m{i}{side}" for i in range(1, 19) for side in ["e", "w"]] +
    [f"j{i}{side}" for i in range(1, 15) for side in ["e", "w"]]
)


def scrape_all_rank_change_details(ranks, csv_filename):
    """
    Writes a CSV containing, for every start_rank & end_rank in all_ranks:
      • One row per win count (0–15) with that entry's total_matches and sanyaku breakdown,
      • One summary row (“TOTAL”) with sum of matches,
      • One separator row of '#'.
    """
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Start Rank", "End Rank", "Wins", "Number of Resulting Banzuke at End Rank", "Sanyaku Results"])

        for start_rank in ranks:
            for end_rank in all_ranks:
                results = scrape_rank_change(start_rank, end_rank)

                total_matches = 0
                for entry in results:
                    wins = entry["wins"]
                    matches = entry["total_matches"]
                    sanyaku_json = json.dumps(entry["sanyaku_results"])

                    writer.writerow([start_rank, end_rank, wins, matches, sanyaku_json])
                    total_matches += matches

                # summary row
                writer.writerow(["", "", "TOTAL", total_matches, ""])
                # separator row
                writer.writerow(["#", "#", "#", "#", "#"])


start_from = "j1e"
# Skip ranks until we reach start_from
start_index = all_ranks.index(start_from)
subset_ranks = all_ranks[start_index:]
# Run for every possible start/end rank
scrape_all_rank_change_details(subset_ranks, "all_rank_change_resultsjuryo.csv")
