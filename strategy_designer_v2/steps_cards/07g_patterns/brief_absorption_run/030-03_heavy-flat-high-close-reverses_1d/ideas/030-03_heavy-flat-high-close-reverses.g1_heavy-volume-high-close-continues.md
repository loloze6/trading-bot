---
brief: 030_absorption-day-close-location
source-idea: 030-03_heavy-flat-high-close-reverses
line: 7.g patterns
backtest: 030-03_heavy-flat-high-close-reverses_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: On a day when a coin's volume is far above its 20-day average, the closer its close sits to the day's high, the more the coin rises over the next 5 days. The effect is larger the heavier that day's volume is.
Consequence: A heavy-volume day that closes near its high is a reason to be long the coin for the following 5 days, and a reason to refuse a short.
Why:
- F1: On heavy-volume days (volume at least 2x the prior 20-day mean, 733 non-overlapping cases), a close near the high is followed by a rise over the next 5 days, the opposite of the tested reversal. The close-location terciles (mean 0.20, 0.55, 0.86) give strengths of 0.009, 0.095 and 0.160 (t 0.13, 1.28, 2.36). The top tercile's unusual move is +1.85 % (t 2.31) and its total move +2.47 % (t 3.09) over 244 cases. That is 13 times the 0.19 % cost of a trade.
- F2: The top-tercile result holds across coins and across the two halves of the record. It is positive in all six coins (BTC 0.237, ETH 0.024, LTC 0.104, XMR 0.088, XRP 0.369, ZEC 0.112). It is positive in both halves (w1–w12 0.178, t 2.08, n 127; w13–w24 0.139, t 1.31, n 117).
- F6: Close location and a prior rise add up. Heavy-volume days after a 5-day rise that close in the top close-location tercile give a strength of 0.205 (t 2.75, n 194). Those in the bottom tercile give 0.045 (t 0.41, n 64).
- F7: The tested score, (close location − 0.5) × volume ratio, is only weakly graded on heavy-volume days. Its quintiles give −0.057, 0.082, 0.090, 0.162 and 0.163. The Pearson correlation is 0.077 (p 0.037) and the Spearman 0.039 (p 0.29).
