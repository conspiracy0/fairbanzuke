import csv

input_file = "all_rank_change_resultsjuryo.csv"
output_file = "filtered_rank_change_resultsjuryo.csv"

with open(input_file, newline='', encoding='utf-8') as infile, open(output_file, 'w', newline='', encoding='utf-8') as outfile:
	reader = csv.reader(infile)
	writer = csv.writer(outfile)

	header = next(reader)
	writer.writerow(header)

	block = []
	keep_block = False

	for row in reader:
		if row == ["#", "#", "#", "#", "#"]:
			if keep_block:
				for r in block:
					writer.writerow(r)
				writer.writerow(row)
			block = []
			keep_block = False
			continue

		if row[2] == "TOTAL":
			total_matches = int(row[3])
			if total_matches != 0:
				keep_block = True
			block.append(row)
		else:
			# skip individual result rows with 0 matches
			if int(row[3]) != 0:
				block.append(row)
