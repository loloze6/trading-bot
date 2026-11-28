---
line: 7.c no effect
backtest: 077-01_falling-calm-deep-close-drift_1d
idea tested: 077-01_falling-calm-deep-close-drift
step 5: no effect
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5404 USD
---
## Findings
- **F1:** In the falling calm profile, the depth below the 20-day high gave no grade at 3 days. The day-clustered slope t was 0.77 on 162 cases over 115 days in the explore half, and 0.23 on 961 cases in step 5. The size was +0.18 % against the idea (t 0.57), which is 0.018 of a usual 7.84 % move, against a trade cost of 0.29 %.
- **F2:** The 20-day depth only separated closes near the high from all the others. Cases below −2 swings moved −1.06 % relative to the coin's drift (126 cases), and those within 2 swings moved +1.23 % (36 cases). Among the deep cases there was no grade (slope t −0.24, 126 cases), and the deepest quintile (−7.8 swings, −0.95 %) did no worse than the middle one (−4.3 swings, −1.85 %).
- **F3:** What carried the continuation was the last few days' fall, not the distance from the 20-day peak. In the profile, the 3-day return in usual swings graded the next 5 days with a clustered t of 2.09 (91 cases, 65 days), and the next 3 days with t 1.56 (162 cases). The 20-day depth reached only t 0.44 and 0.77 on the same cases.
- **F4:** Over the next 5 days, the excess return fell as the past 5-day return got weaker. By quartile of the 5-day return in swings:
- **F5:** The depth below the 5-day high graded the next 5 days more than the 20-day depth did (t 1.41 against 0.44, 91 cases). Over 3 days, its deepest quartile (−3.9 swings) moved −1.98 % and the next one (−2.1 swings) −1.08 %. The two shallower quartiles moved +1.48 % and −0.58 %.
- **F6:** The short-window effect was not even across the data.
- **F7:** The same short-term continuation also showed outside the profile, in the bars the detector sent to "chop" (any other profile). There, the 3-day return graded the next 3 days with t 2.02 (921 cases), and the 20-day depth graded the next 5 days with t 2.54 (563 cases). This argues against the brief's claim that the effect belongs to calm, falling markets only.

## Ideas
- `077-01.c1_short-window-peak-depth-continuation` (from F2, F5, F1): In a falling, calm market, the further a coin's close sits below its highest high of the past 5 days, measured in its standard deviation of daily returns over the past 20 days, the larger its fall over the next five days.
- `077-01.c2_calm-downtrend-fall-continuation` (from F3, F4, F6): In a falling, calm market, the larger a coin's 3-day fall, measured in its standard deviation of daily returns over the past 20 days, the larger its fall over the next five days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
