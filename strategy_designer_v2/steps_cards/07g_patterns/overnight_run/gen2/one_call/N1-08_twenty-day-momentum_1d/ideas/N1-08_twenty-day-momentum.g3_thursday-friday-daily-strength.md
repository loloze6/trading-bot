---
brief: 002_moving-average-cross-trend-persistence
source-idea: N1-08_twenty-day-momentum
line: 7.g patterns
backtest: N1-08_twenty-day-momentum_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's daily return is higher on Thursday and Friday than on the other weekdays.
Consequence: A trader can time long entries to hold through Thursday and Friday, and avoid adding exposure into Monday and Wednesday.
Why:
- F6: Daily excess returns differ by weekday. Thursday and Friday are positive (+0.25%, t=2.63; +0.30%, t=3.76; about 2480 days each), while Monday and Wednesday are negative (-0.24%, t=-2.53; -0.30%, t=-2.70). The pooled Thursday-Friday excess is positive in 7 of 8 years and in all 6 coins (LTC t=3.35).
