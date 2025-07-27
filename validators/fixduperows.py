import os
import csv

input_folder = "../bashoresultsv2"
output_folder = "../editedbashosv2"
os.makedirs(output_folder, exist_ok=True)

for fname in os.listdir(input_folder):
    if not fname.endswith(".csv"):
        continue
    in_path = os.path.join(input_folder, fname)
    out_path = os.path.join(output_folder, fname)
    with open(in_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames
        print(fieldnames)

    # Remove duplicate rows by "Name", preserving first occurrence
    seen_names = set()
    unique_rows = []
    for row in rows:
        if row["Name"] not in seen_names:
            unique_rows.append(row)
            seen_names.add(row["Name"])
        # else: duplicate, skip

    # Rewrite Rank column to be 0, 1, 2, ...
    for i, row in enumerate(unique_rows):
        row["Rank"] = str(i)

    # Write to new output folder
    with open(out_path, "w", newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(unique_rows)
