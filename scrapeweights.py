import requests
from bs4 import BeautifulSoup
import csv, time

# Function to scrape head-to-head weight
def scrape_weight(rank1, rank2):
    winurl = f"https://sumodb.sumogames.de/Query_bout.aspx?show_form=0&rank1={rank1}&onlyw1=on&rank2={rank2}&form1_year=1958-now"
    lossurl = f"https://sumodb.sumogames.de/Query_bout.aspx?show_form=0&rank1={rank1}&onlyl1=on&rank2={rank2}&form1_year=1958-now"
    response = requests.get(winurl)
    lresponse = requests.get(lossurl)
    soup = BeautifulSoup(response.content, "html.parser")
    lsoup = BeautifulSoup(lresponse.content, "html.parser")

    results_text = soup.find(string=lambda text: "results found" in text)
    lresults_text = lsoup.find(string=lambda text: "results found" in text)
    # if results_text and lresults_text:
    wins = int(results_text.strip().split(" ")[0])
    losses = int(lresults_text.strip().split(" ")[0])

    #TODO: exclude fusen losses
    return wins, losses
    # else:
    #     return None, None

# List of all ranks including yokozuna
all_ranks = ['y','o','s','k'] + [f"m{i}" for i in range(1, 19)] + [f"j{i}" for i in range(1, 15)]

# Open CSV file to write
with open("weightswithjuryonewdatelimited.csv", mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    header = ["Rank vs"] + all_ranks
    writer.writerow(header)

    for primary_rank in all_ranks:
        row = [primary_rank.upper()]
        match_counts = []
        weighted_total = 0
        total_matches = 0

        for opponent_rank in all_ranks:
            if len(match_counts) != 0 and len(match_counts) % 8 == 0:
                print("sleeping")
                time.sleep(9)
                print("finished_sleep")
            if primary_rank == opponent_rank:
                row.append("-")
                match_counts.append(0)
                continue

            wins, losses = scrape_weight(primary_rank, opponent_rank)

            if losses != 0:
                weight = (wins/losses)
                row.append(str(weight))
                matches = wins + losses
                match_counts.append(matches)
                weighted_total += matches * weight
                total_matches += matches
                print("got weight of", primary_rank, "vs", opponent_rank, ":", weight, "matches:", matches)
                # time.sleep(0.25)
                # print("finished_sleep")
            else:
                row.append("N/A")
                match_counts.append(0)
                print("N/A")

        weighted_mean = (weighted_total / total_matches) if total_matches else 0
        row.append(f"{weighted_mean:.2f}")
        writer.writerow(row)

        # Write second row with total matches
        match_count_row = ["Total Matches"] + match_counts + [total_matches]
        writer.writerow(match_count_row)

        print("Wrote row for rank", primary_rank, "weighted mean:", weighted_mean)
        # if primary_rank == "y":
        #     break

    # for primary_rank in all_ranks:
    #     row = [primary_rank.upper()]
    #     for opponent_rank in all_ranks:
    #         if primary_rank == opponent_rank:
    #             row.append("-")
    #             continue
    #         wins, losses = scrape_weight(primary_rank, opponent_rank)
    #         weight = str(wins/losses) if losses != 0 else "INF"
    #         if wins is not None and losses is not None:
    #             row.append(weight)
    #         else:
    #             row.append("N/A")
    #         print("got weight of ", primary_rank, "vs ", opponent_rank, ":", weight)
    #         time.sleep(0.5)
    #     writer.writerow(row)
    #     print("Wrote row for rank", primary_rank)

    print("CSV file 'all_ranks_head_to_head.csv' has been created successfully.")
