---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-04_downrun-volume-fade-depth-rebound.b2_dips-in-downtrends-keep-falling
line: 7.g patterns
backtest: 024-04_downrun-volume-fade-depth-rebound.b2_dips-in-downtrends-keep-falling_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: The higher a coin's traded volume over the last day against its own average volume over the past 30 days, the more the coin rises over the next three days, whichever way its price moved during that day.
Consequence: A trader leans long a coin after a day of unusually heavy volume and refuses to be long after a day of unusually thin volume.
Why:
- F1: Each coin rises more over the next 3 days the larger its last day's volume is against its 30-day average volume: the pooled slope of the drift-adjusted 3-day strength on the log volume ratio is +0.103 with t 4.91 over 5004 non-overlapping cases, it is positive in all six coins (t from 0.96 for XMR to 3.49 for XRP) and in all eight years, and it is positive in 75 % of the 24 windows.
- F2: The effect is graded from end to end: in the lowest volume-ratio quintile (mean ratio 0.35) the mean strength is -0.101 (t -3.44, 1001 cases), and in the highest quintile (mean ratio 2.25) it is +0.089 (t 2.48, 1001 cases), with the middle quintiles in between.
- F4: The effect does not depend on the direction of the recent move, which goes against the brief's fading-volume reversal: the slope is +0.098 (t 3.26, 2553 cases) after a rising 3-day return and +0.107 (t 3.61, 2451 cases) after a falling one, and volume times the sign of the move has a slope of -0.012 (t -0.58).
- F5: Grid cells that open on Sunday 00:00 UTC are followed by a weaker 3 days (mean strength -0.150, t -4.05, 811 cases; negative against the rest in all six coins, t from -1.14 to -2.42). They also have the lowest volume ratio (0.72 against 0.83 to 1.22 on other days), and the Sunday dummy loses its effect once volume is in the regression (beta -0.002, t -0.03).
