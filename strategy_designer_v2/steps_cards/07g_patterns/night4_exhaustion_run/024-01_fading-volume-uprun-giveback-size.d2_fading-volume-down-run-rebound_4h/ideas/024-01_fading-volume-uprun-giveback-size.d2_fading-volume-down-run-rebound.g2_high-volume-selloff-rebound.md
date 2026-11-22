---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-01_fading-volume-uprun-giveback-size.d2_fading-volume-down-run-rebound
line: 7.g patterns
backtest: 024-01_fading-volume-uprun-giveback-size.d2_fading-volume-down-run-rebound_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: After a coin's 1-day fall, the higher the volume of its latest 4-hour periods relative to its 30-day norm, the larger its rebound over the next 3 days.
Consequence: A sell-off on heavy volume is a reason to buy for a 3-day rebound; a sell-off on thin volume is a reason to refuse that buy.
Why:
- F3: High volume after a fall is where the effect concentrates. In the top volume fifth, after a 1-day fall the unusual move is +1.38 % (t 3.16); after a 1-day rise it is +0.42 % (t 0.95). In the bottom volume fifth, after a fall it is −0.63 % (t −2.00). The rebound after falls therefore comes with rising volume, the opposite of the tested fading-volume situation.
- F4: The tested idea shows no edge. Its unusual move is +0.00 % (t 0.002, 4537 cases). Raw extremes do rebound: bottom fifth of the 1-day move +0.75 % (t 2.80), bottom fifth of the streak loss in usual moves +0.67 % (t 2.44). These are not graded, because the next fifth is −0.29 % and −0.75 % (t −3.09).
- F1: The level of volume predicts the next 3 days. Cases were read once per 18-bar cell on each coin's grid. When a coin's 3-day mean log volume, against its 30-day norm, is in its top fifth, its unusual 18-bar move is +0.97 % (t 3.13, 1062 cases). In its bottom fifth it is −0.85 % (t −3.44, 1062 cases). The single-bar volume gives the same split: top fifth +1.02 % (t 3.23, strength 0.109), bottom fifth −0.60 % (t −2.64), 1059 cases each.
