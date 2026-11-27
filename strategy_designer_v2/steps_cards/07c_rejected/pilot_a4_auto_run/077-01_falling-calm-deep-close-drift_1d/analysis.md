---
line: 7.c no effect
backtest: 077-01_falling-calm-deep-close-drift_1d
idea tested: 077-01_falling-calm-deep-close-drift
step 5: no effect
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5321 USD
---
## Findings
- **F1:** In the falling calm profile, depth below the 20-day high predicts nothing at any horizon tried, in the plan's measure and in the rebuilt grid. The slope is t 0.11 at 1 day (525 cases), t 0.66 at 3 days (170), t 0.61 at 5 days (101) and t 0.58 at 10 days (50). At 3 days the five depth quintiles, deepest to shallowest, show excess returns of -0.93 %, -0.97 %, -0.27 %, -0.33 % and +0.94 %, and none has |t| above 1.2.
- **F2:** Across the plan's 3-day cases the coins were slightly below their usual drift (mean excess t -0.61, 170 cases), but the shortfall is not tied to depth. The step-5 size is an unusual move of -0.10 % per case (t -0.28 over 470 days), against a cost of 0.33 % per trade.
- **F3:** Depth does carry a continuation effect, but outside the profile and in the plan's direction. In the bars outside falling calm, the d20 slope is t 2.45 at 3 days (801 cases) and t 3.60 at 5 days (486), with the deepest third at -1.28 % and the shallowest at +1.52 % excess over 5 days.
- **F4:** In falling agitated bars, depth over 40 days points the other way, as the brief said it would: the slope is t -1.85 at 3 days and t -1.94 at 5 days. Only 40 and 25 cases support this.
- **F5:** In the recorded falling calm bars, the coin's own 5-day return, in 20-day daily swings, does predict the next days, as continuation. The slope is t 2.17 over 3 days (170 cases) and t 2.78 over 5 days (101). The 3-day return gives t 3.54 over 5 days. Over 5 days the lowest third of the 5-day return has -4.47 % excess and the highest third +0.46 %. Cases with a positive 5-day return (47) average +1.04 % excess and +1.89 % total.
- **F6:** The 5-day-return continuation is broad but not uniform.
- **F7:** The distance of the close above its 20-day low, in the same swings, also grades the next move in falling calm. The slope is t 2.52 over 5 days and t 2.23 over 10 days, with the lowest third at -2.51 % and the highest at +1.82 % excess over 5 days. Recent recovery predicts here, and depth from the peak does not.

## Ideas
- `077-01.c1_falling-calm-recovery-continues` (from F1, F5, F6, F7): In a falling, calm market, while a coin closes below its highest high of the past 20 days, the more its close has risen over the past five days, measured in its standard deviation of daily returns over the past 20 days, the larger its rise over the next five days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
