sekitori_size = 69

url_template = "https://sumodb.sumogames.de/Query_bout.aspx?show_form=0&year=202501&shikona1=Tobizaru&onlyw1=on"
# define the rikishi class
class Rikishi:

    def __init__(self, name, beats):
        self.name = name
        self.beats = beats
        self.wins = len(beats)
        self.losses = 15-self.wins
        self.record = (self.wins-self.losses)*2
        self.neustadl = self.wins
        self.weighted_neustadl = None
        self.rank = None
        self.inverse_rank = None
        self.weight = None
        self.weighted_raw_record = 0
        self.sanyaku = ""



def neustadl_calc(rikishi):
    for opponent in rikishi.beats:
        rikishi.neustadl += opponent.wins

def weighted_raw_calc(rikishi):
     for opponent in rikishi.beats:
        #first, get their regular win/loss with weight
        rikishi.weighted_raw_record += opponent.weight
     rikishi.weighted_neustadl = rikishi.weighted_raw_record

def weighted_neustadl_calc(rikishi):
    for opponent in rikishi.beats:
        rikishi.weighted_neustadl += opponent.weighted_raw_record

# all code comments in lower case

from functools import cmp_to_key

# define a comparison function that implements the described logic:
# return a negative number if 'a' should come before 'b',
# return a positive number if 'a' should come after 'b',
# return 0 if they are considered equal for sorting purposes.
def basic_compare_rikishi(a, b):
    # first check: if a has a higher (rank + record), a should go first
    if a.rank == None:
        print("discarding compare against ", a.name)
        # return 1
        return 100
    elif b.rank == None:
        print("discarding compare against ", b.name)
        return -100

    atruerank = (a.inverse_rank + a.record)
    btruerank = (b.inverse_rank + b.record)
    if atruerank > btruerank:
        return -atruerank
    if atruerank < btruerank:
        return btruerank

    if a.record < 0 and b.record > 0 :
        return 1
    elif b.record < 0 and a.record > 0:
        return -1

    return 0
def advanced_compare(a,b):
    if a.rank == None:
        print("discarding compare against ", a.name)
        # return 1
        return 100
    elif b.rank == None:
        print("discarding compare against ", b.name)
        return -100
     # second check: compare weighted_neustadl
    atruerank = (a.inverse_rank + a.record)
    btruerank = (b.inverse_rank + b.record)
    if atruerank > btruerank:
        return (-1*atruerank)
    if atruerank < btruerank:
        return btruerank

    if a.weighted_neustadl > b.weighted_neustadl:
        return -1
    elif a.weighted_neustadl < b.weighted_neustadl:
        return 1

    #  # third check: compare neustadl
    # if a.neustadl > b.neustadl:
    #     return -1
    # elif a.neustadl < b.neustadl:
    #     return 1


    # fourth check: if b is in a.beats, then a should go before b
    if b in a.beats:
        return -1
    elif a in b.beats:
        # if a is in b.beats, then b should go before a
        return 1

    # if none of the above apply, they are considered equal in this sort
    return 0

def combined_compare(a,b):
     # first check: if a has a higher (rank + record), a should go first
    if a.rank == None:
        print("discarding compare against ", a.name)
        # return 1
        return 100
    elif b.rank == None:
        print("discarding compare against ", b.name)
        return -100

    atruerank = (a.inverse_rank + a.record)
    btruerank = (b.inverse_rank + b.record)
    if atruerank > btruerank:
        return (-1*atruerank)
    if atruerank < btruerank:
        return btruerank

    # if a.record < 0 and b.record > 0 :
    #     return 1
    # elif b.record < 0 and a.record > 0:
    #     return -1

    if a.weighted_neustadl > b.weighted_neustadl:
        return -1
    elif a.weighted_neustadl < b.weighted_neustadl:
        return 1

     # third check: compare neustadl
    # if a.neustadl > b.neustadl:
    #     return -1
    # elif a.neustadl < b.neustadl:
    #     return 1


    # fourth check: if b is in a.beats, then a should go before b
    if b in a.beats:
        return -1
    elif a in b.beats:
        # if a is in b.beats, then b should go before a
        return 1


    return 0

def combined_comparev2(a,b):
     # first check: if a has a higher (rank + record), a should go first
    if a.rank == None:
        print("discarding compare against ", a.name)
        # return 1
        return 100
    elif b.rank == None:
        print("discarding compare against ", b.name)
        return -100

    atruerank = (a.inverse_rank + a.record)
    btruerank = (b.inverse_rank + b.record)

    # if a.record < 0 and b.record > 0 :
    #     return 1
    # elif b.record < 0 and a.record > 0:
    #     return -1

    if (a.weighted_neustadl > b.weighted_neustadl) and (atruerank >= btruerank):
        return (-1*atruerank)
    elif (a.weighted_neustadl < b.weighted_neustadl) and (btruerank >= atruerank):
        return 1

    if atruerank > btruerank:
        return (-1*atruerank)
    if atruerank < btruerank:
        return btruerank

     # third check: compare neustadl
    # if a.neustadl > b.neustadl:
    #     return -1
    # elif a.neustadl < b.neustadl:
    #     return 1


    # fourth check: if b is in a.beats, then a should go before b
    if b in a.beats:
        return -1
    elif a in b.beats:
        # if a is in b.beats, then b should go before a
        return 1


    return 0

def sort_rikishi(rlist, ozeki_plus):
    # separate out rikishi who are in ozeki_plus
    ozeki_list = [r for r in rlist if r.name in ozeki_plus]
    others_list = [r for r in rlist if r.name not in ozeki_plus]

    # sort all ozeki_plus members by record (descending)
    ozeki_sorted = sorted(ozeki_list, key=lambda x: x.record, reverse=True)

    # take the top 3 ozeki based on record
    ozeki_top_3 = ozeki_sorted[:3]
    # the rest of the ozeki_plus go back into the pool of 'others'
    remaining_ozeki = ozeki_sorted[3:]
    combined_others = others_list + remaining_ozeki

    # now sort the non-ozeki (plus any leftover ozeki) using our custom comparison function
    # others_sorted = sorted(combined_others, key=cmp_to_key(basic_compare_rikishi))
    others_sorted = sorted(combined_others, key=cmp_to_key(combined_comparev2))

    # final sorted list: top 3 ozeki first (by record), then everyone else by the custom comparator
    # return ozeki_top_3 + sorted(others_sorted, key=cmp_to_key(advanced_compare))
    return ozeki_top_3 + others_sorted


# example usage:
# final_sorted_list = sort_rikishi(rikishi_list, ozeki_plus)

import csv

ozeki_plus = ['hoshoryu', 'onosato','kotozakura']
rank_to_score_dict = {
    'o1e' : 2,
    'o1w' : 3,
    'o2w' : 4,
    "s1e" : 5,
    "s1w" : 6,
    "k1w" : 8,
    "k1e" : 7,
    "y": 1,
    }
rikishi_list = []
csv_to_open = 'jan2025withsym.csv'
# read csv and create rikishi instances
with open(csv_to_open, 'r', encoding='utf-8') as csv_file:
    reader = csv.reader(csv_file)
    for row in reader:
        # skip empty rows or rows without enough data
        if not row or len(row) < 2:
            continue
        name = row[0].strip().lower()

        # ismakushita = False
        beats = [opponent.strip().lower() for opponent in row[2:] if opponent.strip()]
        rikishi_obj = Rikishi(name, beats)

        rawrank = row[1].strip().lower()
        try:
            rank = int(rawrank)
            rikishi_obj.rank = rank
            irank = (sekitori_size+1-rank)
            rikishi_obj.inverse_rank = irank
            rikishi_obj.weight = irank/sekitori_size
        except Exception as e:
            print("caught makushita or sanyaku")
            #if in sanyaku
            if rawrank in rank_to_score_dict:
                rikishi_obj.rank = rank_to_score_dict[rawrank]
                rikishi_obj.sanyaku = rawrank
                irank = (sekitori_size+1-rikishi_obj.rank)
                rikishi_obj.inverse_rank = irank
                rikishi_obj.weight = irank/sekitori_size
            else:
                rank = rawrank
                rikishi_obj.wins = int(rikishi_obj.beats[0])
                rikishi_obj.neustadl = rikishi_obj.wins
                rikishi_obj.weight = 0
                # ismakushita = True

        # if ismakushita == True:
            print(rikishi_obj.beats)

        rikishi_list.append(rikishi_obj)

# create a dictionary to map names to Rikishi objects for quick lookup
rikishi_dict = {rikishi.name: rikishi for rikishi in rikishi_list}
# print(rikishi_dict)
# replace each string in self.beats with the corresponding Rikishi object
for rikishi in rikishi_list:
    rikishi.beats = [rikishi_dict[opponent] for opponent in rikishi.beats if opponent in rikishi_dict]

#handle neustadl calcs, no rank weights
for rikishi in rikishi_list:
    # print
    neustadl_calc(rikishi)

#assign weighted records to all rikishi
for rikishi in rikishi_list:
    weighted_raw_calc(rikishi)

#now get weighted neustadl
for rikishi in rikishi_list:
    weighted_neustadl_calc(rikishi)

for rikishi in rikishi_list:
    print(rikishi.name, ", ", rikishi.inverse_rank, ", ", rikishi.rank, ", ", rikishi.weight)
# create a sorted copy of rikishi_list based on the neustadl attribute
simple_neustadl_sorted_rikishi = sorted(rikishi_list, key=lambda rikishi: rikishi.neustadl, reverse=True)

# for r in simple_neustadl_sorted_rikishi:
#     print(r.name, r.neustadl)

weighted_neustadl_sorted_rikishi = sorted(rikishi_list, key=lambda rikishi: rikishi.weighted_neustadl, reverse=True)

print("True Merit WEIGHTED neudstal ____")
for r in weighted_neustadl_sorted_rikishi:
    print(r.name, r.weighted_neustadl, r.neustadl )

print("BANZUKE#####")
banzuke = sort_rikishi(rikishi_list, ozeki_plus)
for rikishi in banzuke:
    # print(rikishi.name, rikishi.weighted_neustadl )
    print(rikishi.name)






