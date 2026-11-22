---
brief: 027_panic-days-are-followed-by-a-premium
source-idea: 027-04_panic-delayed-recovery-drift.d2_panic-in-flat-market-continues
line: 7.g patterns
backtest: 027-04_panic-delayed-recovery-drift.d2_panic-in-flat-market-continues_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: After a 4-hour bar that falls by several times the coin's usual 4-hour move, the coin's return over the next 24 hours is higher than usual, the larger the fall in usual moves the larger the rise.
Consequence: A trader would treat a sudden 4-hour plunge as a one-day buying opportunity rather than the start of further weakness.
Why:
- F4: A single 4-hour bar that falls by at least 3 of its usual 4h moves is followed by an unusual move of +1.50 % over the next 24 hours (t 2.32, 118 cases). The bins between -3 and +3 usual moves show between -0.22 % and +0.02 %.
- F1: The coin's 24-hour fall, scaled by its usual 24-hour move, is followed by a graded rebound over the next 24 hours, on non-overlapping 24h cases across all six coins. Falls beyond 2.5 usual moves show an unusual move of +2.22 % (t 4.32, 198 cases). Falls of 1.5 to 2.5 show +0.65 % (t 3.02, 705 cases). Falls of 0.75 to 1.5 show +0.36 % (t 2.98, 1927 cases). Rises of 0 to 1.5 usual moves are followed by -0.14 % to -0.23 % (t -2.28 and -2.19).
- F3: The 24h rebound after falls of more than 0.75 usual moves is positive in every coin. It ranges from +0.31 % (BTC, t 1.66) to +0.85 % (ZEC, t 2.98). It is positive in every year from 2018 to 2025, from +0.16 % (2022, t 0.59) to +1.39 % (2021, t 3.76).
