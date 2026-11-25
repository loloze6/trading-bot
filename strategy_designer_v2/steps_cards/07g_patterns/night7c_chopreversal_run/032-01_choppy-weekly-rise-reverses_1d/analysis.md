---
line: 7.g patterns
backtest: 032-01_choppy-weekly-rise-reverses_1d
idea tested: 032-01_choppy-weekly-rise-reverses
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4016 USD
---
## Findings
- **F1:** After a coin's largest one-day falls (the lowest decile of the day's return over its 30-day daily standard deviation), the next day's return minus the coin's normal one-day drift averages +0.99 % (t 2.30, 699 cases on 227 days), against +0.44 % (t 1.57) in the second decile and between -0.41 % and +0.06 % in deciles 3 to 10.
- **F2:** On down days the rebound grows with the size of the scaled fall: the Spearman correlation of the scaled fall with the next day's unusual move is -0.096 (p 2e-8, n 3456 days, not clustered). By quintile of fall, largest first, the next-day unusual move is +1.005 % (t 2.30), +0.479 % (t 1.70), +0.020 %, -0.043 % and +0.108 %.
- **F3:** The rebound after the largest falls holds across the data shown: it is positive in 11 of 12 windows (w9 alone negative at -0.88 %, w10 +1.79 % with t 4.94), on all 6 coins (from +0.55 % on BTC to +1.42 % on XMR, t 3.05), and in 3 of 4 years (2019 -0.02 %).
- **F4:** The rebound after the largest falls grows with the coin's 30-day volatility rank. By tercile from low to high it is +0.10 % (t 0.18), +0.73 % (t 1.68) and +2.14 % (t 2.33).
- **F5:** The 30-day efficiency ratio does not change the rebound. By tercile it is +0.79 %, +0.83 % and +0.90 %, so the choppy, trendless condition of the brief adds nothing.
- **F6:** The rebound is a one-day effect. The unusual move after the largest falls is +0.99 % over 1 day (t 2.30), +0.59 % over 2 days (t 1.18), +0.84 % over 3 days (t 1.38) and -0.16 % over 7 days (t -0.16), which matches the tested weekly horizon finding nothing.
- **F7:** The tested idea shows no reversal of weekly rises. In the mean_reversion regime, the top quintile of the scaled 7-day return is followed by a long-signed 7-day strength of +0.17 (t 0.72), which is continuation, not reversal. The Spearman correlation of the scaled 7-day return with the next 7-day strength is +0.027 (p 0.41).
- **F8:** The one-day rebound after the largest falls (+0.99 %) is about 5 times the cost of a trade (0.19 %). The tested idea's unusual move was -0.31 % per case, the wrong sign.

## Ideas
- `032-01.g1_large-daily-fall-rebounds` (from F1, F2, F3, F6, F8): The larger a coin's one-day fall compared with its typical daily swing over the past 30 days, the larger its rise over the next day.
- `032-01.g2_agitated-fall-next-day-rebound` (from F4, F1, F2, F5): When a coin's 30-day volatility is high compared with its past year, the rise over the next day after a one-day fall is larger, and it grows with the size of that fall compared with the coin's typical daily swing over the past 30 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
