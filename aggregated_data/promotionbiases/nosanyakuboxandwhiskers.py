import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt

df = pd.read_csv('filtered_rank_change_resultscomplete.csv')

# Prepare columns
df.rename(columns={
    'Number of Resulting Banzuke at End Rank': 'matches',
    'Sanyaku Results': 'sanyaku_json',
    'Wins': 'wins',
    'Start Rank': 'start_rank',
    'End Rank': 'end_rank'
}, inplace=True)

# Filter: only maegashira starts, exclude sanyaku starts
df = df[df['start_rank'].str.startswith('m')]
df = df[~df['start_rank'].str.startswith(('s', 'k'))]  # redundant, but for clarity

df = df[df['wins'] != 'TOTAL']
df = df[df['matches'].astype(int) > 0]

df['matches'] = df['matches'].astype(int)
df['wins']    = df['wins'].astype(int)

# Rank list
all_ranks = (
    [f"s{i}{side}" for i in range(1, 4) for side in ["e", "w"]] +
    [f"k{i}{side}" for i in range(1, 4) for side in ["e", "w"]] +
    [f"m{i}{side}" for i in range(1, 19) for side in ["e", "w"]] +
    [f"j{i}{side}" for i in range(1, 15) for side in ["e", "w"]]
)

records = []
for _, row in df.iterrows():
    try:
        lst = json.loads(row['sanyaku_json'])
    except:
        continue
    total_score = sum(4*r.get('y',0) + 3*r.get('o',0) + 2*r.get('s',0) + r.get('k',0) for r in lst)
    avg_score = total_score / row['matches']
    start_idx = all_ranks.index(row['start_rank'])
    expected_delta = 2 * row['wins'] - 15
    expected_idx   = max(0, min(len(all_ranks)-1, start_idx - expected_delta))

    # Adequate promotion if ended up in sanyaku
    if row['end_rank'].startswith(('s', 'k')):
        signed_diff = 0
    else:
        end_idx = all_ranks.index(row['end_rank'])
        signed_diff = expected_idx - end_idx

    # expand by matches
    records.extend([{'sanyaku_score': avg_score, 'signed_diff': signed_diff}] * row['matches'])

df_expanded = pd.DataFrame(records)

# Bin sanyaku_score into quantiles
df_expanded['sanyaku_bin'] = pd.qcut(df_expanded['sanyaku_score'], q=5, duplicates='drop')
bins = df_expanded['sanyaku_bin'].cat.categories
data = [df_expanded[df_expanded['sanyaku_bin'] == b]['signed_diff'] for b in bins]

# Plot
plt.figure(figsize=(10, 6))
plt.boxplot(data, positions=np.arange(len(bins)), showfliers=False)
plt.axhline(0, color='gray', linewidth=0.8)
plt.xlabel('Avg Weighted Sanyaku Score Bin')
plt.ylabel('Signed Difference in Rank Placement')
plt.title('Rank Placement Error vs Sanyaku Score\n(maegashira only, M→S/K = 0)')
plt.xticks(np.arange(len(bins)), [f"{b.left:.2f}-{b.right:.2f}" for b in bins], rotation=45)
plt.grid(True, axis='y', which='major')
plt.tight_layout()
plt.savefig("sanyaku_vs_rank_error.png", dpi=200, bbox_inches='tight')
