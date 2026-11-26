---
plan: 032-02.b1.e1.e1.e1.e1_marginal-breakouts-keep-rising_1d
idea: 032-02.b1.e1.e1.e1.e1_marginal-breakouts-keep-rising
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: Welch t of excess 20-bar return, small-margin half minus large-margin half: 0.0113047; Welch t: 0.28252 (threshold: confirm t >= 2 with small half rising more and supporting check passing; reject t <= -2)
- Supporting check: forecast-weighted mean excess 20-bar return > 0: 0.035871, passed: True
- Counts: cases: 240, small-margin half: 120, large-margin half: 120
- Decided by: Welch t is between -2 and 2.
- Reading: Cases are the first long bet (forecast rise of at least 2 points, holding-period rule) in each 20-bar grid cell of each window with a full 20-bar return inside the window; the pooled median split puts margins <= median in the small half; the coin's drift is its mean non-overlapping 20-bar return over all its windows.
- Size: unusual move +3.44 % (t 1.65, the cases of one day together: 188 days) per case over 20 bars, 0.130 of the coin's usual move (21.24 %); normal drift in its direction +2.55 %, total +5.99 %; 240 cases
Plan: `steps_cards/03_test_plan/night7c_rangefail_run/plans/032-02.b1.e1.e1.e1.e1_marginal-breakouts-keep-rising_1d.md`
Record: `steps_cards/04_backtest/night7c_rangefail_run/backtests/032-02.b1.e1.e1.e1.e1_marginal-breakouts-keep-rising_1d`
Measure: `measure.py`
