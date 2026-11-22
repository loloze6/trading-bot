---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-01_fading-volume-uprun-giveback-size.g2_calm-strong-advance-continues
line: 7.g patterns
backtest: 024-01_fading-volume-uprun-giveback-size.g2_calm-strong-advance-continues_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: The higher a coin's traded volume over the past day against its average daily volume over the past 30 days, the more the coin rises over the next three days.
Consequence: A day of unusually heavy volume is a reason to hold a long for the next three days, and a quiet day a reason to refuse one.
Why:
- F2: Heavy volume points to a rise. A coin's volume over the past day, as a log ratio to its 30-day average, predicts its 3-day return above drift with slope 0.0094 and t 5.28 (5004 non-overlapping cases). The slope is positive in all six coins (t from 0.96 for XMR to 3.49 for XRP) and in both halves of the windows (w1-12 t 2.68, w13-24 t 4.60).
- F3: The same holds for volume against the day before. Volume over the last 1.5 days against the 1.5 days before also predicts the 3-day return above drift (slope 0.0035, t 2.03, 5580 cases). By quintile it runs from -0.60 % (t -2.34) in the second-lowest to +0.39 % in the highest. This is the opposite of the brief's fading-volume give-back.
- F1: The tested idea earns almost nothing of its own: its unusual move is -0.03 % per case over 3 days (strength -0.006, 4453 cases). The book's gain comes from the coins' drift: its mean daily return is at or below holding the coin for five of six coins (XMR 0.026 % against 0.107 %, ZEC 0.095 % against 0.155 %, ETH 0.106 % against 0.137 %). Only XRP beats holding (0.179 % against 0.130 %).
