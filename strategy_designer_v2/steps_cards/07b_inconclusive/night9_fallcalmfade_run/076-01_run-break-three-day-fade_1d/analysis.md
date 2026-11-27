---
line: 7.b inconclusive
backtest: 076-01_run-break-three-day-fade_1d
idea tested: 076-01_run-break-three-day-fade
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 1
cost: 0.2187 USD
---
## Findings
- **F1:** The fade grows with the run's length, as the idea predicts, and is nil after a single down day. On folds B and C, the short-signed 3-day unusual move is -0.06 % after 1-day runs (t -0.13, 1049 cases). It is +1.07 % after 2-day runs (t 1.55, 569), +1.23 % after 3-day runs (t 1.66, 288), +1.67 % after 4-day runs (t 1.51, 101) and +3.20 % after runs of 5 or more (t 3.03, 79).
- **F2:** The main measure is unclear because single-day runs are about half the cases and add nothing. Over all breaks the unusual move is +0.63 % (t 1.79, 2086 cases, 647 days). Breaks after runs of 3 or more down days alone give +1.66 % over 3 days (t 2.87, 468 cases, 236 days).
- **F3:** The effect is on the predicted side, short of the bar, and spread evenly, not carried by one coin. All six coins are positive, from +0.40 % (XRP, t 0.65) to +0.87 % (XMR, t 1.86). Nine of 12 windows are positive; w11 is the main exception at -3.59 % (t -2.80).
- **F4:** The fade lasts several days after long runs. After runs of 3 or more, the unusual move is +0.96 % at 1 day (t 2.38), +1.66 % at 3 days (t 2.87) and +2.13 % at 5 days (t 2.59), so the plan's 3-day horizon fits.
- **F5:** The fade lives mostly where the coin has been falling over the past 20 days. In the lowest third of 20-day returns the unusual move is +1.52 % (t 2.18, 597 cases). It is +0.07 % in the middle third (t 0.16) and -0.29 % in the top third (t -0.56).
- **F6:** The up day's size matters little, as the brief says. By up-day size thirds the unusual move is +0.32 % (t 0.75) for small up days, +1.19 % (t 2.68) for middle ones and +0.40 % (t 0.62) for large ones, with no rising grade.
- **F7:** Over the coin's normal drift, the total move per case was -0.02 %, against a cost of 0.19 % a trade. A short book can only pay where the fade is large enough to beat the coin's rise, which means after long runs, not on every break.

## Ideas
- `076-01.b1_run-break-fade-all-coins` (from F2, F3, F1): In any market, the first up day after a run of down days is followed by a fall over the next three days, and the fall is larger the more down days the run held.
- `076-01.b2_run-break-fade-in-decline` (from F5, F1, F4, F7): In any market, the first up day after a run of down days, in a coin whose 20-day return is negative, is followed by a fall over the next three days, and the fall is larger the more down days the run held and the deeper the 20-day fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
