---
line: 7.g patterns
backtest: 058-03.g1_calm-downtrend-weekly-continuation_1d
idea tested: 058-03.g1_calm-downtrend-weekly-continuation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3944 USD
---
## Findings
- **F1:** Inside the falling calm profile the next 5 days follow the last 5 days in steps: by quintile of the 5-day return the excess next-5-day return runs -2.47 % (t -1.68, 71 cases), -2.46 % (t -2.09, 70), -0.66 % (t -0.62), +0.29 % (t 0.29) and +2.39 % (t 1.39, 71). Outside the profile the same quintiles run -0.68, -0.85, +0.40, +0.61, +0.11 % (all |t| < 1.3, about 244 cases each), so the continuation sits in the calm downtrend.
- **F2:** The continuation inside the profile is carried by the falls more than by the rises. After a 5-day fall the signed continuation is +2.81 % (t 2.33, 65 cases) on low volume, +0.70 % (t 0.63, 51) on middle volume and +2.71 % (t 1.94, 58) on high volume. After a 5-day rise it is +0.48 % (t 0.32), +1.49 % (t 1.04) and +0.30 % (t 0.20).
- **F3:** Heavy volume does not weaken the continuation after a fall, against the brief. The high-volume tercile's +2.71 % is about the same as the low-volume tercile's +2.81 %.
- **F4:** The depth of the past weeks does not grade the next 5 days inside the profile. By quartile of the 20-day return, from the deepest fall to the shallowest, the excess next-5-day return is -1.25 % (t -1.15), -2.62 % (t -2.48), -1.68 % (t -1.60) and +0.31 % (t 0.28): no steady gradient from the deepest falls.
- **F5:** The book earns mostly from its short bars inside the profile:
- **F6:** The book gains on the coins in falling windows and gives up much of the coins' rise in rising windows:
- **F7:** Over all bars, the next day's return is high after Thursday's close (+0.565 %, t 3.86) and after Friday's close (+0.533 %, t 3.88), with about 1,190 bars each. Cases on the same day across coins are not grouped here, so these t overstate. The map already holds a late-week gain (045-01, in rising markets), and I could not read this effect by profile, so it is not a discovery here.

## Ideas
- `058-03.g1.g1_calm-downtrend-weekly-fall-continues` (from F1, F2, F3, F5): In a falling, calm market, a coin that has fallen over its last 5 days keeps falling over the next 5 days, and the further it has fallen over those 5 days, the more it falls next, whatever the volume of the fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
