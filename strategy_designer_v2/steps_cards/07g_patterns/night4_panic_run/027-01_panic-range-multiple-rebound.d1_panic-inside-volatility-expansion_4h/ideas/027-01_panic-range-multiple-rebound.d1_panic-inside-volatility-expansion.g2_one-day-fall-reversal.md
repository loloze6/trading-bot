---
brief: 027_panic-days-are-followed-by-a-premium
source-idea: 027-01_panic-range-multiple-rebound.d1_panic-inside-volatility-expansion
line: 7.g patterns
backtest: 027-01_panic-range-multiple-rebound.d1_panic-inside-volatility-expansion_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: The deeper a coin's fall over the past 24 hours, the more it earns above its usual return over the next 24 hours.
Consequence: A trader would lean into sharp one-day drops for a one-day rebound; at about 0.12 of a usual daily move, this should be enough to clear the 0.19 % cost of a trade.
Why:
- F1: The panic premium is real but short. The bottom quintile of 24-hour return (mean fall -6.1 %) was followed by a strength of +0.118 of a usual move over the next 24 hours (t 5.88, 3450 non-overlapping cases) and +0.084 over the next 3 days (t 2.45, 1116 cases). It was gone by 7 days (-0.010, t -0.20, 462 cases) and reversed at 14 days (-0.117, t -2.09, 204 cases). So the tested 14-day horizon sits where the premium has already disappeared.
- F2: The 24-hour reversal holds everywhere. The rank correlation between the 24-hour return and the next 24 hours' strength was negative in all 6 coins (-0.070 to -0.148) and in all 8 years (-0.037 to -0.178). Top-minus-bottom quintile ranged from -0.05 to -0.31, with Welch t as low as -4.54 (XMR) and -4.96 (2018).
