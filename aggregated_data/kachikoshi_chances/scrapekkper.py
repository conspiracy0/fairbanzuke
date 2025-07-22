import requests
from bs4 import BeautifulSoup
import csv, time

#0 = only get full wrestled bouts
#1 = take all absences
#2 = ignore only full absences
def scrape_kk(rank, ignore_absences=0):
    mkurl = ""
    kkurl = ""
    if ignore_absences > 0:
        mkurl = f"https://sumodb.sumogames.de/Query.aspx?show_form=0&form1_rank={rank}&form1_wins=mk&form1_year=1958-now&rowcount=5"
        kkurl = f"https://sumodb.sumogames.de/Query.aspx?show_form=0&form1_rank={rank}&form1_wins=kk&form1_year=1958-now&rowcount=5"
    else:
        mkurl = f"https://sumodb.sumogames.de/Query.aspx?show_form=0&form1_rank={rank}&form1_wins=0-7&form1_losses=15-8&form1_year=1958-now"
        kkurl = f"https://sumodb.sumogames.de/Query.aspx?show_form=0&form1_rank={rank}&form1_wins=15-8&form1_losses=0-7&form1_year=1958-now"
    response = requests.get(kkurl)
    lresponse = requests.get(mkurl)
    soup = BeautifulSoup(response.content, "html.parser")
    lsoup = BeautifulSoup(lresponse.content, "html.parser")

    results_text = soup.find(string=lambda text: "results found" in text)
    lresults_text = lsoup.find(string=lambda text: "results found" in text)

    kkamount = int(results_text.strip().split(" ")[0])
    mkamount = int(lresults_text.strip().split(" ")[0])

    if ignore_absences == 2:
        table = lsoup.find("table", class_="record")
        rows = table.find_all("tr")
        for row in rows[2:]:
            cells = row.find_all("td")
            record = cells[3].get_text()
            # print(record.count("-"))
            recordlist = record.split('-')
            if len(recordlist) > 2:
                if recordlist[2] == "15":
                    mkamount -= 1

        # for cell in cells:
            # print(cell.get_text())

    #TODO: exclude fusen losses
    return kkamount, mkamount


all_ranks = ['y','o','s','k'] + [f"m{i}" for i in range(1, 19)] + [f"j{i}" for i in range(1, 15)]
def get_kkresults(filename, ignore_absences=0):

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # write header row
        writer.writerow(["rank", "kk_amount", "mk_amount", "kk_pct"])

        for rank in all_ranks:
            # scrape number of kachikoshi and makekoshi
            kk_amount, mk_amount = scrape_kk(rank, ignore_absences)

            # calculate percentage chance of kachikoshi
            total = kk_amount + mk_amount
            kk_pct = kk_amount/total

            # write the data row
            writer.writerow([rank, kk_amount, mk_amount, round(kk_pct, 4)])

            # be polite to the server
            time.sleep(1)

        print("Wrote", filename)


get_kkresults("kkresultsignorefullabsences.csv", 2)
get_kkresults("kkresultsgetabsences.csv", 1)
