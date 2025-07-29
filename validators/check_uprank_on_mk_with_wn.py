import os
import csv

folder = "../fairbanzukeoutputnofixes"  # replace with your actual folder name

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
            if ("S" in row["New Rank Title"] or "K" in row["New Rank Title"]) and "M" in row["Old Rank Title"] and int(row["Wins"]) < 8:
                correct.append((fname, row["Name"]))
                trigger = True
                # break
            # names.append(row["Name"])
        # if not trigger:
        #     incorrect.append(fname)

print("Correct:")
for n in correct:
    print(n)
print("Incorrect")
for n in incorrect:
    print(n)
