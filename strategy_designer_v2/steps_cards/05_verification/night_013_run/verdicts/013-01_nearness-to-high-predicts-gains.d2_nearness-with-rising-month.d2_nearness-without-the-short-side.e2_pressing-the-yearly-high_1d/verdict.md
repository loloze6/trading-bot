---
plan: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e2_pressing-the-yearly-high_1d
idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e2_pressing-the-yearly-high
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: top-quintile mean 7-bar excess return over holding: 0.00923535; t of the mean: 1.23579 (threshold: t >= 2 confirms (with supporting check), t <= -2 rejects; at least 100 top-quintile cases)
- Supporting check: top minus fourth quintile mean 7-bar return, Welch t > 0: 0.674643, passed: True
- Counts: top-quintile cases: 476, fourth-quintile cases: 475, grid cases: 2378, active bars: 17044
- Decided by: The top-quintile mean excess over holding has t = 1.24, between -2 and 2.
- Reading: The situation is graded and centred on the coin's usual distance, as the Fidelity states, so each active bar's expected side is the sign of (dist_high after standardise + the plan's +10 offset): long when the close is nearer its 52-week high than usual, short when it is farther; a bar counts only if its raw distance is valid (<= 0); the top and fourth quintiles are cut at the 80th and 60th percentiles of the pooled grid forecasts (top: >= q80, fourth: q60 <= f < q80); holding is the coin's mean 7-bar return over all its grid bars in all windows; fewer than 100 top-quintile cases gives 'not observable'.
- Size: unusual move +2.25 % per case over 7 bars, 0.169 of the coin's usual move (12.44 %); normal drift in its direction +0.24 %, total +2.48 %; 357 cases
Plan: `steps_cards/03_test_plan/night_013_run/plans/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e2_pressing-the-yearly-high_1d.md`
Record: `steps_cards/04_backtest/night_013_run/backtests/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e2_pressing-the-yearly-high_1d`
Measure: `measure.py`
