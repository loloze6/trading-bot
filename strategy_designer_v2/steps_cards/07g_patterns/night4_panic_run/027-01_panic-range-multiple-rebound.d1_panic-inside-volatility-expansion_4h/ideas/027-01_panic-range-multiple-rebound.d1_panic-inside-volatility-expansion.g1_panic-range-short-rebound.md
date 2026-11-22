---
brief: 027_panic-days-are-followed-by-a-premium
source-idea: 027-01_panic-range-multiple-rebound.d1_panic-inside-volatility-expansion
line: 7.g patterns
backtest: 027-01_panic-range-multiple-rebound.d1_panic-inside-volatility-expansion_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: When a coin has fallen over the past 24 hours, the larger its 24-hour high-low range as a multiple of its average 24-hour range over the past 30 days, the more it earns above its usual return over the next 3 days.
Consequence: A trader would buy the widest-range panics for a few days and not hold them for two weeks, since the premium is spent within days.
Why:
- F1: The panic premium is real but short. The bottom quintile of 24-hour return (mean fall -6.1 %) was followed by a strength of +0.118 of a usual move over the next 24 hours (t 5.88, 3450 non-overlapping cases) and +0.084 over the next 3 days (t 2.45, 1116 cases). It was gone by 7 days (-0.010, t -0.20, 462 cases) and reversed at 14 days (-0.117, t -2.09, 204 cases). So the tested 14-day horizon sits where the premium has already disappeared.
- F3: Among 24-hour falls, only the largest range multiples were followed by a premium over the next 3 days. The top quintile (range 2.26 times the 30-day mean) had a strength of +0.210 (t 4.01, 399 cases), while the other four quintiles lay between -0.057 and +0.007. Over 14 days the same top quintile gave +0.003 (t 0.03, 73 cases), with no grading across quintiles.
- F4: The range-multiple grading among falls is robust over 24 hours and mostly holds over 3 days. Over 24 hours its rank correlation with strength was positive in all 6 coins (0.056 to 0.137) and all 8 years (0.069 to 0.117). Over 3 days it was positive in 6 of 6 coins (0.022 to 0.130) and 6 of 8 years, with 2020 top-minus-bottom +0.608 (t 3.63).
- F5: Volatility expansion adds little at the tested horizon. The top quintile of the 7-day/60-day volatility ratio gave +0.161 over 14 days (t 1.37, 90 cases) and +0.093 over 3 days (t 1.96, 570 cases). This matches the verdict's -0.012 strength over 84 bars, despite a passed top-minus-bottom check (+1.25 %).
