import requests
from bs4 import BeautifulSoup
import time
import csv
from functools import cmp_to_key
class Rikishi:

    def __init__(self, name, beats):
        self.name = name
        self.beats = beats
        self.wins = len(beats)
        self.losses = 15-self.wins
        self.record = (self.wins-self.losses)*2
        # self.record = (self.wins-self.losses)
        self.neustadl = self.wins
        self.weighted_neustadl = None
        self.rank = None
        self.inverse_rank = None
        self.weight = None
        self.sanyaku = ""
        self.weighted_raw_record = 0
        self.sanyaku_out = ""
        self.badrankprevent_new_rank = None

import csv

sanyakutitles = {
    "Yokozuna 1 East": "Y1e",
    "Yokozuna 1 West": "Y1w",
    "Ozeki 1 East": "O1e",
    "Ozeki 1 West": "O1w",
    "Ozeki 2 East": "O2e",
    "Ozeki 2 West": "O2w",
    "Ozeki 3 East": "O3e",
    "Ozeki 3 West": "O3w",
    "Sekiwake 1 East": "S1e",
    "Sekiwake 1 West": "S1w",
    "Sekiwake 2 East": "S2e",
    "Sekiwake 2 West": "S2w",
    "Komusubi 1 East": "K1e",
    "Komusubi 1 West": "K1w",
    "Komusubi 2 East": "K2e",
    "Komusubi 2 West": "K2w",
}
# CSV export function
def export_rikishi_to_csv(rikishi_list, filename="rikishi_results.csv"):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Write CSV header
        writer.writerow([
            "Name", "Wins", "Losses", "Record",
            "Neustadl", "Weighted Neustadl", "Rank",
            "Inverse Rank", "Weight", "Sanyaku", "Beats",
        ])

        # Write Rikishi data line-by-line
        for rikishi in rikishi_list:
            writer.writerow([
                rikishi.name,
                rikishi.wins,
                rikishi.losses,
                rikishi.record,
                rikishi.neustadl,
                rikishi.weighted_neustadl if rikishi.weighted_neustadl is not None else "",
                rikishi.rank if rikishi.rank is not None else "",
                rikishi.inverse_rank if rikishi.inverse_rank is not None else "",
                rikishi.weight if rikishi.weight is not None else "",
                rikishi.sanyaku,
                 ";".join(rikishi.beats),  # Joins opponents by semicolon
            ])

def import_rikishi_from_csv(filename="rikishi_results.csv"):
    rikishi_list = []
    with open(filename, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            name = row["Name"]
            beats = row["Beats"].split(';') if row["Beats"] else []
            rikishi = Rikishi(name, beats)
            rikishi.record = int(row["Record"])
            # rikishi.neustadl = row["Neustadl"]
            rikishi.wins = int(row["Wins"])
            rikishi.losses = int(row["Losses"])
            rikishi.weighted_neustadl = float(row["Weighted Neustadl"]) if row["Weighted Neustadl"] else None
            rikishi.rank = int(row["Rank"]) or None
            rikishi.inverse_rank = int(row["Inverse Rank"])
            rikishi.weight = float(row["Weight"]) if row["Weight"] else None
            # print(rikishi.weight)
            rikishi.sanyaku = row["Sanyaku"]
            # print(row)

            rikishi_list.append(rikishi)
    return rikishi_list


def scrape_sumodb(suffix, csvname):
    BASE_URL = "https://sumodb.sumogames.de/"
    TARGET_URL = f"{BASE_URL}{suffix}"

    # Get the main page
    response = requests.get(TARGET_URL)
    soup = BeautifulSoup(response.content, "html.parser")

    # Locate the "Makuuchi Banzuke" table
    # tables = soup.find_all("table")
    tables = soup.find_all("table", class_="banzuke")

    rikishi_list = []
    rank_counter = 0



    for table in tables:

        # if not "Makuuchi" in table.get_text():
        #     break
        if "Sandanme" in table.get_text():
            # makuuchi_table = table
            break
    #
    # if makuuchi_table is None:
    #     print("Makuuchi Banzuke table not found.")
    #     exit()

        rows = table.find_all("tr")
        header_cells = [cell.get_text(strip=True) for cell in rows[0].find_all(['th'])]

        # result_index = header_cells.index("Result")
        result_indices = [i for i, cell in enumerate(header_cells) if cell == "Result"]
        # print(result_index)
        # print(header_cells)


        for row in rows[1:]:
            cells = row.find_all("td")
            print("#####row#####")
            print(result_indices)
            for idx in result_indices:
                print("#####idx######")
                print(idx)
                if len(cells) > idx:


                    # print("cell ", str(idx), ": ", cells[idx])
                    if idx == 0:
                        #fix break if there is no east side
                        if cells[1].find("a" )== None:
                            continue
                        name = cells[1].find("a").get_text(strip=True)
                    else:
                        name = cells[3].find("a").get_text(strip=True)
                    print(name)
                    result_cell = cells[idx]
                    link_tag = result_cell.find("a")
                    opp_beat = []
                    rank = ""
                    if link_tag and 'href' in link_tag.attrs:
                        #get beats info
                        url = f"{BASE_URL}{link_tag['href']}"
                        wrestler_page = requests.get(url)
                        # print(url)
                        # print(wrestler_page)
                        # print(cells)
                        wrestler_soup = BeautifulSoup(wrestler_page.content, "html.parser")
                        titlerank = wrestler_soup.find("td", class_="rb_topleft").contents[0]

                        results_table = wrestler_soup.find("table", class_="rb_torikumi")
                        # print(results_table)
                        # print(results_table.get_text())

                        wrestler_rows = results_table.find_all("tr")
                        for wrestler_row in wrestler_rows:
                            wrestler_cells = wrestler_row.find_all("td")
                            # print("#######")
                            # print(wrestler_cells[1])
                            img = wrestler_cells[1].find('img')['src']
                            if "shiro" in img or "fusensho" in img:
                                # print("found won")
                                opp_beat.append(wrestler_cells[3].find("a").get_text(strip=True).split()[1])
                            # if "kuro" in img or "fusenpai" in img:
                            #     print("found loss")

                        rikishi_obj = Rikishi(name, opp_beat)
                        if titlerank in sanyakutitles.keys():
                            rikishi_obj.sanyaku = sanyakutitles[titlerank]
                        rikishi_obj.rank = rank_counter
                        rank_counter += 1
                        rikishi_obj.inverse_rank = 70-rikishi_obj.rank
                        #don't weight makushita wrestlers
                        rikishi_obj.weight = rikishi_obj.inverse_rank/70 if rikishi_obj.rank <= 70 else 0
                        rikishi_list.append(rikishi_obj)
                        print(rikishi_obj.name, ", ", rikishi_obj.inverse_rank, ", ", rikishi_obj.rank, ", ", rikishi_obj.weight, ", ", rikishi_obj.beats)
                        if rank_counter % 10 == 0:
                            print("sleeping to avoid rate timeout")
                            time.sleep(10)

                    else:
                        print("failed somehow due to link fucking up")
                        # return
                        # links.append()
                        # print(link_tag['href'].strip())
                print("#####end idx######")
            print("####end row###")

    for rikishi in rikishi_list:
        print(rikishi.name, ", ", rikishi.inverse_rank, ", ", rikishi.rank, ", ", rikishi.weight, ", ", rikishi.beats)

    export_rikishi_to_csv(rikishi_list, csvname)


def fill_in_rikishi_list_data(rikishi_list):
    # create a dictionary to map names to Rikishi objects for quick lookup
    rikishi_dict = {rikishi.name: rikishi for rikishi in rikishi_list}
    for rikishi in rikishi_list:
        rikishi.beats = [rikishi_dict[opponent] for opponent in rikishi.beats if opponent in rikishi_dict]

    #handle simple neustadl calcs, and add
    for rikishi in rikishi_list:
        # print
        for opponent in rikishi.beats:
            rikishi.neustadl += opponent.wins
            # print(rikishi.name)
            rikishi.weighted_raw_record += opponent.weight

        #base score is all the weights of opponents you beat
        rikishi.weighted_neustadl = rikishi.weighted_raw_record

    #assign weighted records to all rikishi
    for rikishi in rikishi_list:
        for opponent in rikishi.beats:
            #final score is all the weights of opponents you beat, and the weights of all the opponents
            #your opponent beat
            rikishi.weighted_neustadl += opponent.weighted_raw_record

        print(rikishi.name, rikishi.weighted_neustadl)

    return rikishi_list

def simple_neustadl_banzuke(rikishi_list):
    return sorted(rikishi_list, key=lambda rikishi: rikishi.neustadl, reverse=True)


def weighted_neustadl_banzuke(rikishi_list):
    return sorted(rikishi_list, key=lambda rikishi: rikishi.weighted_neustadl, reverse=True)

sekiwake_vals = ['S1e', 'S1w', 'S2e', 'S2w']
def sort_non_ozeki_raw_compare(a, b):

    #true rank is the "true placement" they should be at given their rank and record. i.e, a M8e with a 8-7 should go to M7e

# if (a.weighted_neustadl > b.weighted_neustadl) and (atruerank >= btruerank):
    #     return (-1)
    # elif (a.weighted_neustadl < b.weighted_neustadl) and (btruerank >= atruerank):
    #     return 1

    atruerank = (a.inverse_rank + a.record)
    btruerank = (b.inverse_rank + b.record)

    #first, if one wrestler has a higher weighted neustadl, and are also at a higher or equal true rank,
    #then that wrestler should always be before the other wrestler
    #this means that if you had a harder tournament, and are at the same true rank or better than another wrestler, you should always be higher than them

    #if you don't meet the first criteria, if you had a better true rank than another wrestler, you should be in front of them at all times
    if atruerank > btruerank:
        return (-1)
    if atruerank < btruerank:
        return 1

    if (a.weighted_neustadl > b.weighted_neustadl):
        return (-1)
    elif (a.weighted_neustadl < b.weighted_neustadl):
        return 1


    # # final tiebreak, f b is in a.beats, then a should go before b
    # if b in a.beats:
    #     return -1
    # elif a in b.beats:
    #     # if a is in b.beats, then b should go before a
    #     return 1
    print("returning 0 on ", a.name, "vs", b.name)
    return 0
def sort_non_ozeki_raw(rlist):
    return sorted(rlist, key=cmp_to_key(sort_non_ozeki_raw_compare))

def sort_non_ozeki_no_spurious_ranks(a, b):

    atruerank = a.inverse_rank + a.record
    btruerank = b.inverse_rank + b.record

    # Check for negative record conditions first
    a_negative = a.wins < 8
    b_negative = b.wins < 8


    # Original comparator logic continues
    if atruerank > btruerank and not a_negative:
        return -1
    if atruerank < btruerank and not b_negative:
        return 1

    # Neustadl tiebreaker
    if a.weighted_neustadl > b.weighted_neustadl:
        return -1
    elif a.weighted_neustadl < b.weighted_neustadl:
        return 1

    # Optional beats-based tiebreaker:
    # if b in a.beats:
    #     return -1
    # elif a in b.beats:
    #     return 1

    return 0
#prevent downranking if the rikishi has a kk after raw weighted neustadl evaluation
def prevent_downrank_with_kk(sorted_rikishi, offset):
    #offset is the index offset from the first rank to the first index of the list we are given
    final_ranking = sorted_rikishi.copy()

    for i, rikishi in enumerate(sorted_rikishi):
        # Only proceed if rikishi had at least 8 wins
        if rikishi.wins >= 8:
            print("detected wins")
            # Check if their new rank is worse (numerically higher) than their original
            if (i + offset) > rikishi.rank:
                # Move rikishi up to their original rank
                print("detected spurious downrank @ ", rikishi.name, rikishi.rank)
                final_ranking.pop(i)
                print(rikishi.rank - offset)
                final_ranking.insert(rikishi.rank - offset, rikishi)

    return final_ranking

#prevent someone from upranking with a makekoshi
def prevent_uprank_with_mk(sorted_rikishi, offset):
    # Assume rikishi.original_rank is their initial rank before sorting (e.g., M3 => 3)

    final_ranking = sorted_rikishi.copy()
    #
    # for i, rikishi in enumerate(sorted_rikishi):
    #     if (i+offset <= 70 and rikishi.wins < 8) or (i+offset> 70 and rikishi.wins < 4):
    #         if (i+offset) < rikishi.rank:
    #              print("detected spurious uprank @ ", rikishi.name, rikishi.rank, i+offset)
    #              # for j in range(i, len(sorted_rikishi):
    #              final_ranking.pop(i)
    #              final_ranking.insert(rikishi.rank+1-offset, rikishi)


    # Iterate backwards to avoid conflicts when modifying the list
    # for i in reversed(range(len(sorted_rikishi))):
    #     rikishi = sorted_rikishi[i]
    #     if rikishi.wins < 8:  # Makekoshi
    #         # print("detected mk")
    #         # If their new rank (i+1) is better (lower) than original, move them back down
    #         if (i + 1 + offset) < rikishi.rank:
    #             print("detected spurious uprank @ ", rikishi.name, rikishi.rank)
    #             # Remove rikishi from current position
    #             final_ranking.pop(i)
    #             # Reinsert rikishi at their original rank (or lowest available position)
    #             insert_pos = rikishi.rank - 1 + offset
    #             # Ensure insert position isn't beyond list length
    #             insert_pos = min(insert_pos, len(final_ranking))
    #             final_ranking.insert(insert_pos, rikishi)

    # final_ranking now ensures no rikishi with losing records are promoted

    return final_ranking

#sanyaku heuristics:
#0 = no heuristics, will not attempt to determine sekiwakes etc
#1 = fair, simple heuristics
#2 = prevent downranking
def make_banzuke(rikishi_list,filename, use_sanyaku_heuristics=1):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        yokozuna_list = []
        ozeki_list = []
        komusubi_list = []
        sekiwake_list = []

        for rikishi in rikishi_list[:]:  # Iterate over a shallow copy
            if rikishi.sanyaku in ['O1e', 'O1w', 'O2e', 'O2w', 'O3e', 'O3w']:
                ozeki_list.append(rikishi)
                rikishi_list.remove(rikishi)
            elif rikishi.sanyaku in ['S1e', 'S1w', 'S2e', 'S2w']:
                sekiwake_list.append(rikishi)
                # rikishi_list.remove(rikishi)
            elif rikishi.sanyaku in ['Y1e', 'Y1w']:
                yokozuna_list.append(rikishi)
                rikishi_list.remove(rikishi)
            elif rikishi.sanyaku in ['K1e', 'K1w', 'K2e', 'K2w']:
                komusubi_list.append(rikishi)
                # rikishi_list.remove(rikishi)


        #first, handle yokozuna and ozeki, which are simply based on who has the best record
        #TODO prio1 make this change with use_sanyaku_heuristics
        #TODO handle ties in record
        yokozuna_sorted = sorted(yokozuna_list, key=lambda x: x.record, reverse=True)
        ozeki_sorted = sorted(ozeki_list, key=lambda x: x.record, reverse=True)

        #TODO make this fit more yokozuna and ozeki
        #TODO handle kadoban
        writer.writerow(
            [item for i, rikishi in enumerate(yokozuna_sorted)
                for item in (rikishi.name, "Y1e" if i == 0 else "Y1w")]
        )
        writer.writerow(
            [item for i, rikishi in enumerate(ozeki_sorted)
                for item in (rikishi.name, "O1e" if i == 0 else "O1w")]
        )

        #figure out who's in the joi

        # joi_list = []
        # #find joi minimum
        # joi_min = 10000
        # for rikishi in rikishi_list:
        #     #if the wrestler is sanyaku, ignore
        #     if rikishi.sanyaku != "":
        #         continue
        #     joi_min = min(joi_min, int(rikishi.rank))
        #
        # #now we know the first ranked rikishi that wasn't sanyaku
        # for rikishi in rikishi_list:
        #     if int(rikishi.rank) >= joi_min and int(rikishi.rank) < joi_min+8:
        #         joi_list.append(rikishi)

        # sorted_joi_list = sorted(joi_list, key=lambda x: int(x.rank))
        # print([rikishi.name for rikishi in sorted_joi_list])
        # return

        #TODO handle sekiwake promotion criteria

        sorted_list = sort_non_ozeki_raw(rikishi_list)
        final_sekiwake_out = []
        #do heuristics to determine who gets the sekiwake slots
        # print("pop " , sorted_list.pop(0).name)
        if use_sanyaku_heuristics > 0:
            for rikishi in sorted_list[:]:
                #first, if someone was already a sekiwake, and posted a kachikoshi, they are a sekiwake
                if rikishi in sekiwake_list and rikishi.record > 0:
                    final_sekiwake_out.append(rikishi)
                    sorted_list.remove(rikishi)
                    continue

                #if a komusubi gets at least 11 wins, move him to sekiwake
                if rikishi in komusubi_list and rikishi.wins >= 11:
                    final_sekiwake_out.append(rikishi)
                    sorted_list.remove(rikishi)
                    continue


            #if there are 2 sekiwake now, hooray, we are done
            #if not, we figure out who is doing the best in terms of their true rank (true rank = rank + wins) (this will always be the first person(s) on the sorted list remaining), then add them to the sekiwake list
            if len(final_sekiwake_out) < 2:
                while(len(final_sekiwake_out) < 2):
                    final_sekiwake_out.append(sorted_list.pop(0))


            #now, sort the sekiwake rankings
            #if we are in fair mode, simply assign them based on true rank
            #if we are using more unfair heuristics, apply them instead


            #now, sort the sekiwake ranking based on true rank
            final_sekiwake_out = sorted(final_sekiwake_out, key=cmp_to_key(sort_non_ozeki_raw_compare))
            if use_sanyaku_heuristics == 2:
                offset = len(yokozuna_list) + len(ozeki_list)
                final_sekiwake_out = prevent_downrank_with_kk(final_sekiwake_out, offset)
                final_sekiwake_out = prevent_uprank_with_mk(final_sekiwake_out, offset)


            sekiwake_prefix = "S"
            sekiwake_number = 1
            for i in range(0, len(final_sekiwake_out), 2):
                east = final_sekiwake_out[i]
                west = final_sekiwake_out[i + 1] if i + 1 < len(final_sekiwake_out) else None

                row = [east.name, f"{sekiwake_prefix}{sekiwake_number}e"]

                if west:
                    row.extend([west.name, f"{sekiwake_prefix}{sekiwake_number}w"])
                else:
                    row.extend(["", ""])  # Fill blanks if odd number of rikishi

                # Write row to CSV
                writer.writerow(row)

                # Print to terminal clearly with weighted_neustadl score
                if west:
                    print(f"{row[1]}: {row[0]} ({east.weighted_neustadl}) | {row[3]}: {row[2]} ({west.weighted_neustadl})")
                else:
                    print(f"{row[1]}: {row[0]} ({east.weighted_neustadl}) | {row[3]}: (empty)")

                sekiwake_number += 1  # Increment sekiwake rank each iteration

        #TODO: make non-heuristic out for sekiwake (doable with just changing the final sorted list out)


            #Next, figure out who our komusubi are
            final_komusubi_out = []
            for rikishi in sorted_list[:]:
                #first, check if there are any komusubi remaining with a kachikoshi. They are still komusubi
                if rikishi in komusubi_list and rikishi.record > 0:
                    final_komusubi_out.append(rikishi)
                    sorted_list.remove(rikishi)
                    continue


            previous_ranks_offset = len(yokozuna_list) + len(ozeki_list) + len(final_sekiwake_out) + len(final_komusubi_out)
            for rikishi in sorted_list[:]:
                truerank = rikishi.inverse_rank+rikishi.record
                komusubi_threshold = 70 - previous_ranks_offset
                #for every individual who WOULD have made it past the threshold for komusubi with their true rank, simply put them in as new slots
                if truerank >= komusubi_threshold:
                    final_komusubi_out.append(rikishi)
                    sorted_list.remove(rikishi)

            #prevent downranks and upranks
            final_komusubi_out = sorted(final_komusubi_out, key=cmp_to_key(sort_non_ozeki_raw_compare))
            if use_sanyaku_heuristics == 2:
                offset = len(yokozuna_list) + len(ozeki_list) + len(final_sekiwake_out)
                final_komusubi_out = prevent_downrank_with_kk(final_komusubi_out, offset)
                final_komusubi_out = prevent_uprank_with_mk(final_komusubi_out, offset)


            komusubi_prefix = "K"
            komusubi_number = 1
            for i in range(0, len(final_komusubi_out), 2):
                east = final_komusubi_out[i]
                west = final_komusubi_out[i + 1] if i + 1 < len(final_komusubi_out) else None

                row = [east.name, f"{komusubi_prefix}{komusubi_number}e"]

                if west:
                    row.extend([west.name, f"{komusubi_prefix}{komusubi_number}w"])
                else:
                    row.extend(["", ""])  # Fill blanks if odd number of rikishi

                # Write row to CSV
                writer.writerow(row)

                # Print to terminal clearly with weighted_neustadl score
                if west:
                    print(f"{row[1]}: {row[0]} ({east.weighted_neustadl}) | {row[3]}: {row[2]} ({west.weighted_neustadl})")
                else:
                    print(f"{row[1]}: {row[0]} ({east.weighted_neustadl}) | {row[3]}: (empty)")

                komusubi_number += 1  # Increment komusubi rank each iteration


        #now, finally handle maegashira
        offset = len(yokozuna_list) + len(ozeki_list) + len(final_sekiwake_out) + len(final_komusubi_out)
        #
        if use_sanyaku_heuristics == 2:
            trouble_list = []
            for i in range(len(sorted_list)):
                rikishi = sorted_list[i]

                if (i+offset <= 70 and rikishi.wins < 8 and i+offset < rikishi.rank):
                    trouble_list.append(rikishi)

            finalized_list = []
            final_list = sorted_list.copy()
            for i in range(len(sorted_list)):
                rikishi = sorted_list[i]

                if rikishi in trouble_list:
                    # Wrestler must not move above their original position
                    original_pos = rikishi.rank-offset+1

                    current_pos = 0
                    for i in range(len(final_list)):
                        if final_list[i] == rikishi:
                            current_pos = i
                            break


                    # If they're ranked better now (lower index) than their original rank, move them down
                    while current_pos <= original_pos:
                        print("found", rikishi.name)
                        print(current_pos, original_pos)
                        # Swap downward with wrestler below
                        # if current_pos+1> len(sorted_list):
                        #     finalized_list.append(rikishi)
                        #     break
                        print("###")
                        print(final_list[current_pos].name)
                        swap_index = current_pos+1

                        # if
                        # while (final_list[swap_index] in finalized_list):
                        #     swap_index += 1
                        final_list[current_pos], final_list[swap_index] = (
                            final_list[swap_index],
                            final_list[current_pos],
                        )
                        print(final_list[current_pos].name)

                        current_pos += 1
                    finalized_list.append(rikishi)


        rank_prefix = "M"
        rank_number = 1  # Start with M1
        makuuchi_limit = 42

        for i in range(0, len(final_list), 2):
            current_rank_position = offset + i

            # Switch to Juryo ranks if we've reached the limit
            if current_rank_position >= makuuchi_limit:
                rank_prefix = "J"
                rank_number = 1 + (current_rank_position - makuuchi_limit) // 2

            east = final_list[i]

            # Short circuit if this rank crosses the makuuchi boundary
            if rank_prefix == "M" and current_rank_position + 1 >= makuuchi_limit:
                print("hit shortcirc")
                rank_prefix = "J"
                rank_number = 1
                row = [east.name, f"{rank_prefix}{rank_number}e", "", ""]
                writer.writerow(row)
                print(f"{row[1]}: {row[0]} ({east.weighted_neustadl}) ({east.inverse_rank+east.record}) | {row[3]}: (empty)")
                rank_number += 1
                continue

            west = final_list[i + 1] if i + 1 < len(final_list) else None

            row = [east.name, f"{rank_prefix}{rank_number}e"]

            if west:
                row.extend([west.name, f"{rank_prefix}{rank_number}w"])
            else:
                row.extend(["", ""])

            writer.writerow(row)

            if west:
                print(f"{row[1]}: {row[0]} ({east.weighted_neustadl}) ({east.inverse_rank+east.record}) | {row[3]}: {row[2]} ({west.weighted_neustadl}) ({west.inverse_rank+west.record})")
            else:
                print(f"{row[1]}: {row[0]} ({east.weighted_neustadl}) | {row[3]}: (empty)")

            rank_number += 1  # Increment rank after each row





#
rlist = fill_in_rikishi_list_data(import_rikishi_from_csv("rikishi_resultsrecent.csv"))
make_banzuke(rlist, "testout.csv", 2)

# "Banzuke.aspx?b=202503"
# scrape_sumodb('Banzuke.aspx?b=202211', "kyushu2022.csv")

