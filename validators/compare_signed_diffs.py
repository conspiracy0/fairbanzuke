import os
import csv

folder = "fairbanzukeoutput"  # replace with your actual folder name

for fname in os.listdir(folder):
    if not fname.endswith(".csv"):
        continue
    path = os.path.join(folder, fname)
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        signed_diff_sum = 0
        for row in reader:
            if "M" in row["New Rank Title"] and "M" in row["Old Rank Title"]:
                signed_diff_sum += int(row["Signed Diff"])

        print(fname, signed_diff_sum)
