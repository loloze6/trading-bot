---
brief: 027_panic-days-are-followed-by-a-premium
source-idea: 027-04_panic-delayed-recovery-drift
line: 7.g patterns
backtest: 027-04_panic-delayed-recovery-drift_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: The further a coin's 24-hour return falls below zero, measured in its usual 24-hour moves, the more the coin rises above its normal drift over the next 1 to 3 days.
Consequence: The liquidity premium after a sharp fall is collected by buying at once and holding a few days, not by waiting a day and holding two weeks.
Why:
- F1: The panic premium is real but short and immediate. In each coin's bottom fifth of 24-hour returns measured in usual 24-hour moves (median -1.13), the next day's unusual move averages +0.094 of a usual move (t 4.91, 3268 non-overlapping cases), and the next 3 days' averages +0.070 (t 2.26). By 7 days it is gone (-0.041, t -0.91), and by 14 days it is negative (-0.079, t -1.35).
- F2: The bounce follows the size of the fall. Next-day strength across 24-hour-return fifths, from largest fall to largest rise, is +0.094, +0.010, -0.033, -0.038, -0.047; the last is t -2.56, so large 24-hour rises are followed by a below-usual next day.
- F5: The tested forecast arrives after the bounce. On bars where it is active, the next 3 days average -0.040 of a usual move (t -2.22, 2839 cases) and the next 14 days -0.070 (t -1.39, 504). Raw panic readings, sorted into fifths among non-zero values, show no rising pattern at 14 days (-0.125, +0.009, +0.027, -0.225, -0.070).
