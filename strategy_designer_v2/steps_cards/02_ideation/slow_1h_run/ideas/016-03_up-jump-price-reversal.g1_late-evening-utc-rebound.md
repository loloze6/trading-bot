---
brief: 016_grind-versus-jump-moves
source-idea: 016-03_up-jump-price-reversal
line: 7.g patterns
backtest: 016-03_up-jump-price-reversal_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The more a coin has fallen over the 24 hours up to the 20:00 UTC close, the more it rises over the next 2 hours.
Consequence: A late-evening UTC long is better paid the deeper the day's fall before it, and is a reason to avoid shorting into that window.
Why:
- F1: Every coin rises in the two hours from 21:00 to 23:00 UTC: the mean hourly return is 0.00043 to 0.00056 per coin (t 3.0 to 4.6), against all other hours Welch t = 8.16, and it is positive in 7 of 8 years (2022: -0.00022, t -1.46). Measured from the 20:00 UTC close, the next 2 hours return 0.000966 (t 9.03, n 17261), while the same 2-hour span from the 08:00 close returns -0.000086 (t -0.82).
- F2: That late-evening rise grows with the coin's fall over the 24 hours to the 20:00 UTC close. In the lowest 24-hour-return quintile the next 2 hours return 0.00217 (t 6.65, n 3455), against 0.00068 and 0.00066 in the next two quintiles and -0.000006 in the fourth. The top quintile also returns 0.00132 (t 4.81), so the gradient is clean only on the falling side.
