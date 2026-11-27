---
line: 7.g patterns
backtest: 032-01.b1_calm-fall-continuation-all-coins_1d
idea tested: 032-01.b1_calm-fall-continuation-all-coins
step 5: no effect
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3412 USD
---
## Findings
- **F1:** In the falling calm profile, the next-day unusual return shows no grading by the 30-day return: the quintiles of the 30-day return run from +0.32 % (deepest falls, mean -31 %) to -0.54 %, -0.68 %, +0.19 % and +0.47 % (least fallen, mean +11 %), with no quintile at |t| above 1.4 and a Spearman rho of -0.005 (p 0.90, 477 cases). The tested idea's absence of effect holds on the bars themselves.
- **F2:** No other in-profile situation grades the next-day move. Spearman rho on the next-day unusual return is +0.004 for the 10-day return (547 cases), +0.004 for the 5-day return (566), -0.068 for the day's own return (p 0.10, 590), +0.025 for the place in the 30-day range (484), -0.037 for the close in the day's range (597), +0.004 for the range against its 20-day mean (527) and -0.001 for volume against its 20-day mean (527).
- **F3:** Over longer horizons the picture is the same. On the 3-day grid, rho is +0.028 for the 30-day return, +0.133 for the 5-day return (p 0.07, 184 cases) and +0.116 for the place in the 30-day range (p 0.15, 155). On the 5- and 10-day grids, the 30-day return, the 60-day return and the place in the 30-day range give rho between -0.08 and +0.20, all with p of 0.05 or more and only 31 to 94 cases. Their mean unusual returns have t from -0.28 to +0.37.
- **F4:** The isolated bucket extremes do not line up into a gradient, so they are not findings.
- **F5:** Monday has a next-day unusual return of -1.03 % in profile against the other weekdays (Welch t -2.09, 84 cases), while outside the profile it is -0.04 % (t -0.23, 450). This is one weekday of seven, at t about 2, after many angles, so it is not distinguishable from chance.
- **F6:** The profile's bars are few and concentrated.

## Ideas
- No ideas: Across the forecast, the past 5- to 60-day returns, the place in the 30-day range, the day's shape, range and volume, weekdays, years and windows, no pattern in falling calm markets is graded or stands out beyond what about 100 looks would give by chance (best |t| about 2.7 on a non-monotonic bucket, F4 and F5). No pattern supports a long idea, and the tested move per case (-0.22 %) is below the 0.33 % a trade costs.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
