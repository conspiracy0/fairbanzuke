# Fair Banzuke Maker

This repository contains the alpha version of the **Fair Banzuke Maker** for Grand Sumo. It automatically scrapes information from the SumoDB for each basho (tournament) and generates a banzuke based on predefined, transparent criteria.

---

## Methodology

The primary goal of this algorithm is to minimize arbitrary decision-making and rank wrestlers exclusively based on their in-tournament performance.

### Step 1: Initial Sorting

Each rikishi (wrestler) is initially sorted into a raw banzuke using a custom comparator sort function based on their tournament performance:

- Determine each rikishi’s **true rank**: the position directly resulting from their win-loss record (e.g., a rikishi at Maegashira 6 East with a 9-6 record moves up to Maegashira 3 East, three slots higher).
- Resolve ties using the [**Neustadtl Sonneborn-Berger Score**](https://en.wikipedia.org/wiki/Sonneborn%E2%80%93Berger_score#Neustadtl_Sonneborn%E2%80%93Berger_score) (adapted for drawless sumo tournaments):

$$
N_i = W_i + \sum_{j \in O_i} W_j
$$

Where:
- \( N_i \): Neustadtl score for rikishi \( i \)
- \( W_i \): Number of wins by rikishi \( i \)
- \( O_i \): Set of opponents defeated by rikishi \( i \)
- \( W_j \): Number of wins by opponent \( j \)

A higher Neustadtl score ranks a rikishi higher, rewarding victories over stronger opponents.

### Step 2: Determining Sanyaku

Currently, there is no logic implemented for promotions or demotions involving the ranks of Ozeki or Yokozuna. Rankings within these categories rely purely on tournament records.

#### Sekiwake Criteria:
- Rikishi already ranked Sekiwake with a kachikoshi (winning record) retain their rank.
- Komusubi achieving at least 11 wins are promoted to Sekiwake.

If fewer than two Sekiwake are identified through these criteria, the next highest-ranked wrestlers from the raw banzuke fill the remaining Sekiwake slots.

> **TODO:** Implement a secondary comparator sort exclusively for Sekiwake.

#### Komusubi Criteria:
- Komusubi with a kachikoshi retain their rank.
- Wrestlers whose true rank after the tournament surpasses Komusubi are promoted to Komusubi, even if this exceeds the standard two-slot limit.

> **TODO:** If fewer than two Komusubi are found, select the next highest-ranked wrestlers from the raw banzuke.

### Step 3: Filling Maegashira and Juryo Slots

- Remaining rikishi are placed into Maegashira and Juryo ranks based on their true rank (Step 1).
- Perform a validation pass to ensure no wrestler moves upward in rank following a makekoshi (losing record), except when a rank has been removed (e.g., Maegashira 18 to Maegashira 17 if Maegashira 18 no longer exists).

---

## Known Issues and Planned Features

- **Promotion/Demotion Logic**: Currently lacks rules for Ozeki promotion/demotion and Yokozuna promotion.
- **Weighted Neustadtl Scores**: Does not currently account for the relative value of wins over higher or lower-ranked opponents. Infrastructure for \"Weight-Ranked Neustadtl\" exists, but a satisfactory weighting system is still under development.

Potential weighting solutions under consideration include:
- Weighted mean of expected wins/losses per bout by rank.
- Incorporating historical performance data of individual rikishi.

---

