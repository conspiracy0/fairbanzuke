import os
import csv

folder = "../fairbanzukeoutput"  # replace with your actual folder name

total_sum = []
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
        total_sum.append(signed_diff_sum)

folder = "../fairbanzukeoutputnofixes"
raw_total_sum = []
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
        raw_total_sum.append(signed_diff_sum)


# print("Raw total sum:", raw_total_sum, "Heuristic total sum: ", total_sum)
import statistics
print("Raw total median:", statistics.median(raw_total_sum), "Heuristic total median: ", statistics.median(total_sum))
print("Raw total mean:", statistics.mean(raw_total_sum), "Heuristic total mean: ", statistics.mean(total_sum))
