---
line: 7.g patterns
backtest: N2-04_slow-and-fast-momentum.e1_short-horizon-dual-momentum-continuation_1h
idea tested: N2-04_slow-and-fast-momentum.e1_short-horizon-dual-momentum-continuation
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.4307 USD
---
## Findings
- **F1:** A large 24-hour fall is followed by a rebound over the next day: in the lowest decile of the coins' 24-hour return (mean -8.6 %), the next 24 hours beat the coin's mean 24-hour return by +0.93 % (t 5.56, 1713 non-overlapping cases), while the middle deciles sit between -0.17 % and +0.09 % (|t| < 1.7).
- **F2:** The 24-hour reversal holds in every coin and nearly every year: the correlation of the past 24-hour return with the next 24-hour excess return is negative in all six coins (-0.064 for XRP to -0.129 for XMR, about 2,760 to 2,870 cases each) and in 7 of 8 years (-0.037 to -0.164; only 2024 is positive, at +0.008).
- **F3:** The reversal depends on volatility: the same correlation is -0.107 in the highest tercile of 30-day volatility, -0.038 in the middle tercile and -0.003 in the lowest (about 4,300 cases each), and scaling the fall by volatility still leaves the lowest quintile at +0.47 % next-day excess (t 4.36, 2588 cases).
- **F4:** The reversal also shows at the hourly scale: after the lowest quintile of one-hour returns, the next hour beats the coin's mean by +4.68 bp (t 9.75, 83,303 cases), against -2.45 bp after the highest quintile (t -5.46).
- **F5:** The reversal is gone by three days: on the non-overlapping 72-hour grid, the 72-hour excess return by quintile of the past 24-hour return ranges from -0.37 % to +0.35 % with all |t| < 1.6, about 1,130 cases each.
- **F6:** The 20:00 and 21:00 UTC hours earn +4.83 bp and +3.74 bp over the coin's mean hourly return (t 5.98 and 4.85, about 17,400 cases each), with t between 2.5 and 3.9 in each of the six coins; the effect is negative in 2022 (-2.80 bp), and 13:00 UTC is negative at -4.18 bp (t -4.46).
- **F7:** Saturday's coin return beats the coin's mean daily return by +0.34 % (t 4.08, 2484 days), and the book's best weekdays are Friday (+0.15 %, t 4.50) and Saturday (+0.19 %, t 4.70).
- **F8:** The book earns from a few long holds: the longest fifth of trades (15.8 days on average) gains +26.0 % net with 83 % winners, while the three shortest fifths (under 1 day) each lose 1.3 % to 1.7 % net with 10 % to 26 % winners.
- **F9:** The forecast's size grades the outcome only weakly: the top forecast quintile has a 72-hour excess return of +1.31 % (t 2.11, 372 cases) against -0.32 % in the bottom quintile (t -0.72), and the middle quintiles are not ordered.

## Ideas
- `N2-04_slow-and-fast-momentum.e1_short-horizon-dual-momentum-continuation.g1_one-day-fall-rebound` (from F1, F2, F3, F5): The larger a coin's fall over the past 24 hours, the more its return over the next 1 day exceeds its average daily return, and the effect is stronger the higher the coin's 30-day volatility.
- `N2-04_slow-and-fast-momentum.e1_short-horizon-dual-momentum-continuation.g2_hourly-fall-rebound` (from F4): The larger a coin's fall over the past hour, the more its return over the next hour exceeds its average hourly return.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
