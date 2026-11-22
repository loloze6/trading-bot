---
brief: 027_panic-days-are-followed-by-a-premium
source-idea: 027-04_panic-delayed-recovery-drift.d2_panic-in-flat-market-continues
line: 7.g patterns
backtest: 027-04_panic-delayed-recovery-drift.d2_panic-in-flat-market-continues_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: After a 24-hour stretch in which the coin falls by several of its usual 24-hour moves while its 24-hour range is wider than its usual 24-hour range, the coin's return over the next 3 days is higher than usual, the larger the more the fall and the range multiple exceed their usual size together.
Consequence: A trader would buy a coin after a wide-range 24-hour drop and hold it for about 3 days rather than two weeks, and refuse to short such a drop.
Why:
- F1: The coin's 24-hour fall, scaled by its usual 24-hour move, is followed by a graded rebound over the next 24 hours, on non-overlapping 24h cases across all six coins. Falls beyond 2.5 usual moves show an unusual move of +2.22 % (t 4.32, 198 cases). Falls of 1.5 to 2.5 show +0.65 % (t 3.02, 705 cases). Falls of 0.75 to 1.5 show +0.36 % (t 2.98, 1927 cases). Rises of 0 to 1.5 usual moves are followed by -0.14 % to -0.23 % (t -2.28 and -2.19).
- F2: Among those falls, the range sets the size of the rebound. Falls whose 24h range is in the widest third, measured in usual 24h ranges, show +1.19 % over the next 24 hours (t 6.00, 929 cases) and +2.49 % over the next 3 days (t 5.23, 313 cases). The two narrower thirds show only +0.22 % (t 1.39 and 1.20) over 24h, and -0.02 % (t -0.05) and +0.50 % (t 0.92) over 3 days.
- F3: The 24h rebound after falls of more than 0.75 usual moves is positive in every coin. It ranges from +0.31 % (BTC, t 1.66) to +0.85 % (ZEC, t 2.98). It is positive in every year from 2018 to 2025, from +0.16 % (2022, t 0.59) to +1.39 % (2021, t 3.76).
- F5: At the tested 13-day horizon the panic signal is not graded.
