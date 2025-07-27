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
            if int(row["New Rank"]) < 0:
                incorrect.append(fname)
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
