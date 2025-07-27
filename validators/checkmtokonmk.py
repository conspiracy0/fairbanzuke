import os
import csv

folder = "../fairbanzukeoutput"  # replace with your actual folder name

correct = []
incorrect = []
for fname in os.listdir(folder):
    if not fname.endswith(".csv"):
        continue
    path = os.path.join(folder, fname)
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        trigger = False

        for row in reader:
            if "M" in row["Old Rank Title"] and ("K" in row["New Rank Title"] or "S" in row["New Rank Title"]) and int(row["Wins"]) < 8:
                incorrect.append((fname, row["Name"]))
                trigger = True
                break
            if "K1w" in row["Old Rank Title"] and ("K1e" in row["New Rank Title"] or "S" in row["New Rank Title"]) and int(row["Wins"]) < 8:
                incorrect.append((fname, row["Name"]))
                trigger = True
                break
            if "K" in row["Old Rank Title"] and "S" in row["New Rank Title"] and int(row["Wins"]) < 8:
                incorrect.append((fname, row["Name"]))
                trigger = True
                break
        if not trigger:
            correct.append(fname)


print("Correct:")
for n in correct:
    print(n)
print("Incorrect")
for n in incorrect:
    print(n)

