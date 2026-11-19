---
line: 7.g patterns
backtest: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-uptrend-continuation_1h
idea tested: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-uptrend-continuation
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5618 USD
---
## Findings
- **F1:** The book loses because of its fees, not its direction: on every coin the hourly fee cost (0.58 to 1.31 bp) is larger than the hourly gross gain of the position (-0.26 to +0.54 bp), at 5.6 trades per day, so the daily book return is negative on all six coins (-0.00058 to -0.0037).
- **F2:** In 24-hour steps on a non-overlapping grid, a coin's past 24-hour return in volatility units predicts reversal only when its 7-day volatility is high against its 60-day volatility: the slope of the next 24-hour excess return on the past return is -0.080 (t -5.37, n 4309) in the top tercile of that ratio, +0.006 (t 0.38) in the middle tercile and +0.060 (t 2.60) in the bottom tercile, and the interaction of past return with the volatility ratio has t -5.70 (n 12926).
- **F3:** The high-volatility-ratio reversal is the same sign on all six coins, with slopes from -0.052 (ETH, t -1.40) to -0.128 (ZEC, t -3.46), and in 7 of 8 years, from -0.045 (2024) to -0.247 (2018, t -5.82); the only positive year is 2020 (+0.030, t 0.67).
- **F4:** Within the high-volatility-ratio tercile the effect is graded across the five quintiles of the past 24-hour return: the next 24-hour excess return falls steadily from +1.21% (t 5.31) after the largest falls to +0.43% (t 2.41), then -0.20% and -0.15%, and -0.53% (t -2.53) after the largest rises.
- **F5:** Using the 7-day volatility level alone gives the same split: the reversal slope is -0.087 (t -6.64) in the highest volatility tercile against +0.054 (t 2.70) in the lowest, while the unconditional slope by coin stays between t -2.25 and +1.00.
- **F6:** Hours 20:00 and 21:00 UTC carry a positive drift: the mean hourly return there is 4.2 to 5.5 bp against 0.0 to 0.5 bp in the other hours, with t from 2.66 to 4.10 on each of the six coins. The drift shows in 6 of 8 years; 2022 is the exception (-2.2 bp). Hour 20 alone reaches t 6.75 among the 24 hours tested. I could not turn this into a graded idea.
- **F7:** The tested forecast's edge sits at long horizons and at its high end: over 240 hours the top forecast quintile's excess return is +5.03% (t 2.55, n 168) against -1.75% (t -1.52) for the bottom quintile. Over 24 hours the top quintile's excess return is only +0.21% (t 1.50), too small to pay for the hourly rebalancing in F1. Long trades gain +0.75% gross each and short trades lose 0.12%.

## Ideas
- `001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-uptrend-continuation.g1_volatility-burst-daily-reversal` (from F2, F3, F4, F5): When a coin's volatility over the last 7 days is high relative to its volatility over the last 60 days, the larger its 24-hour return measured in units of its recent volatility, the more the coin moves the opposite way over the next 24 hours, and the reversal is stronger the higher that volatility ratio.
- `001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-uptrend-continuation.g2_calm-market-daily-continuation` (from F2, F5): When a coin's volatility over the last 7 days is low relative to its volatility over the last 60 days, the larger its 24-hour return measured in units of its recent volatility, the further the coin moves the same way over the next 24 hours.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
