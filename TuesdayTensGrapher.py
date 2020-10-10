# Most code written by Bohverkill
# Graphing and general usability added by hOREP.

import json
import re
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
MY_DISCORD_ID = input("Enter Discord ID: ")


RANK_REGEXP = re.compile('^\[.+] ')


class Player:
    def __init__(self, discord_id, name, times_played_with=0, times_played_against=0):
        self.discord_id = discord_id
        self.name = self._parse_name(name)
        self.times_played_with = times_played_with
        self.times_played_against = times_played_against

    @staticmethod
    def _parse_name(name: str) -> str:
        return RANK_REGEXP.sub('', name)

    def __hash__(self) -> int:
        return hash(self.discord_id)

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Player):
            return self.discord_id == o.discord_id
        return False

    def __repr__(self) -> str:
        return 'Player({}, {}, {}, {})'.format(self.discord_id, self.name, self.times_played_with,
                                               self.times_played_against)


with open(input("Enter json file name, e.g. hOREP.json: "), 'r') as f:
    data = json.load(f)
    played_with = []
    played_against = []
    for l in data:
        g = l['GameObject']
        p1 = list(map(lambda x: Player(x['Discord Id'], x['PlayerName']), g['Team1 Players']))
        p2 = list(map(lambda x: Player(x['Discord Id'], x['PlayerName']), g['Team2 Players']))
        if any(x.discord_id == MY_DISCORD_ID for x in p1):
            played_with.extend(p1)
            played_against.extend(p2)
        else:
            played_with.extend(p2)
            played_against.extend(p1)
    played_with = Counter(played_with)
    played_against = Counter(played_against)

    teams = []
    for p, c in played_with.most_common():
        p.times_played_with = c
        teams.append(p)

    for p, c in played_against.most_common():
        d = next((t for t in teams if t == p), None)
        if not d:
            d = p
            teams.append(d)
        d.times_played_against = c

    del teams[0]
    print(teams)


name_list = []
with_list = []
against_list = []

for k in teams:
    name_list.append(k.name)
    with_list.append(k.times_played_with)
    against_list.append(k.times_played_against)

ind = np.arange(len(name_list))
width = 0.3

N = max(max(with_list), max(against_list))  # Largest num played with/against


fig, ax = plt.subplots(figsize=(12, 10))  # Creates (large) figure and axes
# Creates horizontal bar chart of with, and then against
rects1 = ax.barh(ind, with_list, width, color='#0a78ff',
                 align="center", label="Teammate", edgecolor="black")
rects2 = ax.barh(ind + width, against_list, width, color='#ffad0a',
                 align="center", label="Enemy", edgecolor="black")
urname = input("Write your name: ")
ax.set_xlabel('Player Frequency')
ax.set_title(f"{urname}s teammates over {len(data)} games")
# Gives space between bars
ax.set_yticks(ind + width / 2)
ax.set_xticks(ind)
ax.set_yticklabels(name_list)
for i in range(N+1):  # Adds vertical lines corresponding to player freq.
    ax.axvline(i, color='grey', alpha=0.25)

# Limits graph to largest number.
plt.ylim(-1, len(name_list)+1)
plt.xlim(0, N)
plt.legend()
plt.tight_layout()
plt.savefig("BetterPlayerFreqGraph.png", dpi=500)
plt.show()
