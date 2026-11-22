---
line: 7.g patterns
backtest: 024-04_downrun-volume-fade-depth-rebound.b2_dips-in-downtrends-keep-falling_4h
idea tested: 024-04_downrun-volume-fade-depth-rebound.b2_dips-in-downtrends-keep-falling
step 5: rejected
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4360 USD
---
## Findings
- **F1:** Each coin rises more over the next 3 days the larger its last day's volume is against its 30-day average volume: the pooled slope of the drift-adjusted 3-day strength on the log volume ratio is +0.103 with t 4.91 over 5004 non-overlapping cases, it is positive in all six coins (t from 0.96 for XMR to 3.49 for XRP) and in all eight years, and it is positive in 75 % of the 24 windows.
- **F2:** The effect is graded from end to end: in the lowest volume-ratio quintile (mean ratio 0.35) the mean strength is -0.101 (t -3.44, 1001 cases), and in the highest quintile (mean ratio 2.25) it is +0.089 (t 2.48, 1001 cases), with the middle quintiles in between.
- **F3:** Weekly seasonality does not explain the effect, and it shows over a shorter horizon too: with weekday dummies and the 3-day return in the same regression, the volume slope stays at +0.075 (t 3.40); against a same-weekday, same-hour volume baseline from the past four weeks the slope is +0.067 (t 3.65, 5292 cases); over the next 1 day alone the slope is +0.095 (t 4.45).
- **F4:** The effect does not depend on the direction of the recent move, which goes against the brief's fading-volume reversal: the slope is +0.098 (t 3.26, 2553 cases) after a rising 3-day return and +0.107 (t 3.61, 2451 cases) after a falling one, and volume times the sign of the move has a slope of -0.012 (t -0.58).
- **F5:** Grid cells that open on Sunday 00:00 UTC are followed by a weaker 3 days (mean strength -0.150, t -4.05, 811 cases; negative against the rest in all six coins, t from -1.14 to -2.42). They also have the lowest volume ratio (0.72 against 0.83 to 1.22 on other days), and the Sunday dummy loses its effect once volume is in the regression (beta -0.002, t -0.03).
- **F6:** The tested idea's grading by the 30-day return is not there, and the book loses by shorting rising coins: on the grid the slope on the 30-day return is +0.023 (t 1.88), the opposite of a more negative month bringing a deeper fall; the book's daily returns correlate -0.68 with the coins' returns, and it earned -0.0217 % a day while the coins rose 0.067 % to 0.155 % a day.
- **F7:** Neither the streak's size in usual moves nor the volatility level gives a graded forecast of the next 3 days: the streak slope is -0.002 (t -0.40), and the volatility-rank slope is +0.005 (t 0.10).

## Ideas
- `024-04_downrun-volume-fade-depth-rebound.b2_dips-in-downtrends-keep-falling.g1_heavy-volume-precedes-rises` (from F1, F2, F4, F5): The higher a coin's traded volume over the last day against its own average volume over the past 30 days, the more the coin rises over the next three days, whichever way its price moved during that day.
- `024-04_downrun-volume-fade-depth-rebound.b2_dips-in-downtrends-keep-falling.g2_volume-above-weekly-norm-rises` (from F1, F3, F4): The higher a coin's traded volume over the last day against its volume at the same weekday and hours over the past four weeks, the more the coin rises over the next one to three days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
