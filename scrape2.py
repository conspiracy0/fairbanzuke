import requests
from bs4 import BeautifulSoup

BASE_URL = "https://sumodb.sumogames.de/"
# link = "Rikishi_basho.aspx?r=12542&b=202503"
link = "Rikishi_basho.aspx?r=12130&b=202503"
wrestler_page = requests.get(f"{BASE_URL}{link}")
wrestler_soup = BeautifulSoup(wrestler_page.content, "html.parser")

rank = wrestler_soup.find("td", class_="rb_topleft").contents[0]
print(rank)

results_table = wrestler_soup.find("table", class_="rb_torikumi")

# print(table.get_text())
rows = results_table.find_all("tr")
for row in rows[1:]:
    cells = row.find_all("td")
    print("#######")
    print(cells[1])
    img = cells[1].find('img')['src']
    print(img)
    if "shiro" in img or "fusensho" in img:
        print("found won")
    if "kuro" in img or "fusenpai" in img:
        print("found loss")

    opponent = cells[3].find("a").get_text(strip=True).split()[1]
    print(opponent)
    # print(cells[2])
    print("#####end####")
