---
line: 7.g patterns
backtest: 027-04_panic-delayed-recovery-drift.d2_panic-in-flat-market-continues_4h
idea tested: 027-04_panic-delayed-recovery-drift.d2_panic-in-flat-market-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3876 USD
---
## Findings
- **F1:** The coin's 24-hour fall, scaled by its usual 24-hour move, is followed by a graded rebound over the next 24 hours, on non-overlapping 24h cases across all six coins. Falls beyond 2.5 usual moves show an unusual move of +2.22 % (t 4.32, 198 cases). Falls of 1.5 to 2.5 show +0.65 % (t 3.02, 705 cases). Falls of 0.75 to 1.5 show +0.36 % (t 2.98, 1927 cases). Rises of 0 to 1.5 usual moves are followed by -0.14 % to -0.23 % (t -2.28 and -2.19).
- **F2:** Among those falls, the range sets the size of the rebound. Falls whose 24h range is in the widest third, measured in usual 24h ranges, show +1.19 % over the next 24 hours (t 6.00, 929 cases) and +2.49 % over the next 3 days (t 5.23, 313 cases). The two narrower thirds show only +0.22 % (t 1.39 and 1.20) over 24h, and -0.02 % (t -0.05) and +0.50 % (t 0.92) over 3 days.
- **F3:** The 24h rebound after falls of more than 0.75 usual moves is positive in every coin. It ranges from +0.31 % (BTC, t 1.66) to +0.85 % (ZEC, t 2.98). It is positive in every year from 2018 to 2025, from +0.16 % (2022, t 0.59) to +1.39 % (2021, t 3.76).
- **F4:** A single 4-hour bar that falls by at least 3 of its usual 4h moves is followed by an unusual move of +1.50 % over the next 24 hours (t 2.32, 118 cases). The bins between -3 and +3 usual moves show between -0.22 % and +0.02 %.
- **F5:** At the tested 13-day horizon the panic signal is not graded.
- **F6:** The short book lost money: Sharpe -0.43, mean daily return -0.07 %, Calmar -0.36. Its total move per case is -0.78 % against a cost of 0.19 %, because the short side fights a normal drift of -2.01 % in its direction. Holding the coins gained +0.07 % to +0.16 % a day by coin, while the book ranged from -0.29 % to +0.01 % a day.
- **F7:** Bars opening on Friday are followed by +0.40 % over the next 24 hours (t 4.33, 2478 cases). The effect flips sign by year: 2019 +1.38 % (t 5.69), but 2022 -0.60 % (t -2.32) and 2025 -0.33 % (t -1.14). It is not stable enough to count as a finding for an idea.

## Ideas
- `027-04_panic-delayed-recovery-drift.d2_panic-in-flat-market-continues.g1_wide-range-fall-short-rebound` (from F1, F2, F3, F5): After a 24-hour stretch in which the coin falls by several of its usual 24-hour moves while its 24-hour range is wider than its usual 24-hour range, the coin's return over the next 3 days is higher than usual, the larger the more the fall and the range multiple exceed their usual size together.
- `027-04_panic-delayed-recovery-drift.d2_panic-in-flat-market-continues.g2_single-bar-plunge-next-day-rebound` (from F4, F1, F3): After a 4-hour bar that falls by several times the coin's usual 4-hour move, the coin's return over the next 24 hours is higher than usual, the larger the fall in usual moves the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
