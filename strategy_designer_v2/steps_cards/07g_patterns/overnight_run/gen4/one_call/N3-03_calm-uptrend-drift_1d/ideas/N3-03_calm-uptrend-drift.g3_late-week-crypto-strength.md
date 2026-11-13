---
brief: 002_moving-average-cross-trend-persistence
source-idea: N3-03_calm-uptrend-drift
line: 7.g patterns
backtest: N3-03_calm-uptrend-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's daily close-to-close return is higher on Thursdays and Fridays than on Mondays and Wednesdays.
Consequence: Prefer entering longs early in the week and refuse new longs ahead of Monday and Wednesday.
Why:
- F4: Next-day excess return depends on the weekday (about 2,480 one-day cases each). Thursday is +0.0026 (t 2.77) and Friday +0.0035 (t 4.44); Monday is -0.0024 (t -2.47) and Wednesday -0.0033 (t -2.98). The Thu/Fri minus Mon/Wed gap is positive in 7 of 8 years and in all 6 coins (+0.0034 to +0.0074).
