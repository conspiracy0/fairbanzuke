import os
import csv

input_folder = "../bashoresultsv2"
output_folder = "../editedbashosv2"
os.makedirs(output_folder, exist_ok=True)

with open("playofffix.csv", newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    fixrows = list(reader)
    fixfieldnames = reader.fieldnames

    for row in fixrows:
        bcode = row["Date"]
        in_path = os.path.join(input_folder, bcode+".csv")
        print(in_path)
        # out_path = os.path.join(output_folder, fname)
        with open(in_path, newline='', encoding='utf-8') as f2:
            bashoreader = csv.DictReader(f2)
            bashorows = list(bashoreader)
            bashofieldnames = bashoreader.fieldnames
            # print(bashofieldnames)
            for brow in bashorows:
                # print(brow["Name"], row["Winner"])
                if brow["Name"] == row["Winner"]:
                    brow["Beats"] = brow["Beats"].replace(row["Loser"]+";", "").replace(row["Loser"], "")
                    brow["Wins"] = int(brow["Wins"])-1
                    brow["Record"] = brow['Wins'] * 2
#     # Remove duplicate rows by "Name", preserving first occurrence
#     seen_names = set()
#     unique_rows = []
#     for row in rows:
#         if row["Name"] not in seen_names:
#             unique_rows.append(row)
#             seen_names.add(row["Name"])
#         # else: duplicate, skip
#
#     # Rewrite Rank column to be 0, 1, 2, ...
#     for i, row in enumerate(unique_rows):
#         row["Rank"] = str(i)
#
#     # Write to new output folder
#     with open(out_path, "w", newline='', encoding='utf-8') as f:
#         writer = csv.DictWriter(f, fieldnames=fieldnames)
#         writer.writeheader()
#         writer.writerows(unique_rows)
