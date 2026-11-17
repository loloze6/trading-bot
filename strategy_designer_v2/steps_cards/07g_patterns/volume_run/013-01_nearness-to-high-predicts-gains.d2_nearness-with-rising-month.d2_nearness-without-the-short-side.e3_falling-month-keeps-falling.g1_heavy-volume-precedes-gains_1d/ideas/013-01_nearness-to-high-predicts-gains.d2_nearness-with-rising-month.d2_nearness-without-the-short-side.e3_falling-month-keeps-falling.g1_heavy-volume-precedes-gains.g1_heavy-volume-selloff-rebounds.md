---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e3_falling-month-keeps-falling.g1_heavy-volume-precedes-gains
line: 7.g patterns
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e3_falling-month-keeps-falling.g1_heavy-volume-precedes-gains_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The heavier a coin's volume on a day it closes lower, relative to its own 30-day average volume, the higher its return over the next 3 days. The rebound is larger still the bigger that day's drop.
Consequence: A down day on unusually heavy volume is a reason to favour a long in that coin over the next few days, more firmly the heavier the volume and the deeper the drop, while heavy volume on an up day gives no such reason.
Why:
- F1: The tested volume effect comes almost entirely from down days. On days the coin closed lower, the slope of the demeaned 3-day forward return on the 30-day volume ratio is 0.0119 (t = 5.32, n = 2524 non-overlapping cases). On up days it is 0.0009 (t = 0.50, n = 2762). The pooled slope is t = 4.04.
- F2: On down days the effect sits in the heaviest-volume fifth, which is followed by +1.70% demeaned over 3 days (t = 3.74, n = 505). The other four fifths range from −0.56% to −0.03%. Split by both the day's sign and volume, the heaviest down-day fifth gives +1.76%, while the heaviest up-day fifth gives only +0.16%.
- F3: The down-day slope is positive for all six coins, with t from 1.25 (BTC) to 3.21 (XMR) and t of 2 or more for LTC, XMR and ZEC. It is positive in 6 of 8 years, with t ≥ 2.5 in 2020, 2022, 2024 and 2025; 2019 (t −0.12) and 2023 (t −0.58) are the exceptions.
- F4: Weighting the down day by its size also predicts the rebound. The drop's size times the volume ratio has a down-day slope of 0.066 (t = 4.65, n = 2524). The plain 1-day return alone does not predict the 3-day return (slope t = −1.16).
