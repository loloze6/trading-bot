---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-03_uprun-volume-fade-depth-giveback.b2_deep-down-run-rebound
line: 7.g patterns
backtest: 024-03_uprun-volume-fade-depth-giveback.b2_deep-down-run-rebound_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: The larger a coin's 3-day rise in units of its usual 3-day move, the more it keeps rising over the next three days, and the more so the higher its last day's volume stands against its volume over the preceding six days.
Consequence: After a large 3-day rise on surging volume, a trader would buy for a three-day continuation rather than fade the run, because the move per case (about 1 % to 1.6 % on top of the drift) is several times the 0.19 % cost of a trade.
Why:
- F1: The coin's past 3-day return, measured in its usual 3-day moves, grades the next 3 days. On the 18-bar grid the top quintile (mean +1.50 usual moves) is followed by an unusual move of +0.92 % (t 3.10, 1059 cases), against −0.60 % to −0.34 % in quintiles 2 to 4. The rank slope holds on all three grid offsets (t 3.90, 4.46, 5.66, about 5300 cases each). It survives averaging over coins at each date (+0.93 %, t 2.30, 482 dates), and is positive in 6 of 8 years (2020 t 3.02, 2023 t 2.72, 2024 t 2.86).
- F2: Volume rising behind the move adds to it. The top quintile of the ratio of the last bars' volume to the preceding volume is followed by +0.96 % (t 3.63, 1087 cases), against −0.69 % in the second quintile. The ratio keeps t 3.26 next to the past 3-day return in a joint regression. Its rank slope is weaker on the other grid offsets (t 2.17 and 2.08) and averaged by date (t 1.54).
- F3: The strongest cell combines the two: a past 3-day rise in the top quintile with volume in the top tercile is followed by +1.62 %. Among the deepest up-streaks, those with rising volume are followed by +1.09 % (406 cases) and those with fading volume by −0.45 % (256 cases). This is the opposite of the brief's fade-and-give-back.
