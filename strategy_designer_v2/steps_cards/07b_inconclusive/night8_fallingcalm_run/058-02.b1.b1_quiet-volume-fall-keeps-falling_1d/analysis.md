---
line: 7.b inconclusive
backtest: 058-02.b1.b1_quiet-volume-fall-keeps-falling_1d
idea tested: 058-02.b1.b1_quiet-volume-fall-keeps-falling
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3671 USD
---
## Findings
- **F1:** The volume grading the idea rests on is absent. On the fall-regime 5-day grid of folds B and C, the slope of the drift-adjusted return on the forecast is 0.000141 with a day-clustered t of 0.15 (895 cases, 222 days), matching step 5's t of -0.01 on all folds. On the raw 30-day/365-day volume ratio the slope's t is 0.47.
- **F2:** Changing the horizon does not uncover the effect. The slope's t is 0.26 over 3 days (1514 cases, 382 days), 0.15 over 5 days and -0.29 over 10 days. Quiet-volume and other falls earn the same in the short direction over 5 days: +1.07 % (528 cases) against +1.06 % (367 cases).
- **F3:** The effect is also missing in the brief's own falling, calm market. There the slope's t is -0.89 (125 cases, 48 days). Falls on heavier volume continued more there, not less: +3.62 % short excess (15 cases) against +1.86 % for quiet-volume falls (110 cases), the opposite of the brief.
- **F4:** No market profile, year or fall depth shows the grading. The slope's t ranges from -1.41 to +0.84 across the six profiles and from -1.41 to +1.37 across 2018 to 2021, and lies between -0.83 and +0.63 inside each depth tercile.
- **F5:** Depth of fall is not graded either, contrary to the brief's "the more it has fallen, the more it keeps falling". The deepest third of 30-day falls has a short excess of -0.01 % (t -0.02, 229 cases), against +3.63 % for the middle third. The slope of the 5-day excess return on the 30-day return has a t of -0.89 (688 cases).
- **F6:** What remains is a flat, ungraded continuation after any 30-day fall: +0.59 % unusual move per case, t 1.61 over 723 days, 0.047 of a usual move. The coin's drift (-0.70 % in the short direction) cancels it, leaving a total of -0.12 %. That is -0.5 times the 0.22 % cost of a trade, so the book does not pay (Sharpe 0.08, Calmar -0.005).

## Ideas
- No ideas: The theme's effect is not in the data. Neither the lightness of the volume (slope t 0.15 overall, -0.89 in falling calm markets, F1 and F3) nor the depth of the fall (deepest tercile -0.01 %, F5) grades the continuation at any horizon, profile or year tested (F2, F4). The only effect left is an ungraded continuation smaller than the cost of a trade (F6).

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
