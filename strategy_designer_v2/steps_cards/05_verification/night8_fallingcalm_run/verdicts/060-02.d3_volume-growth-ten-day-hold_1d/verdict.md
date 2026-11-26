---
plan: 060-02.d3_volume-growth-ten-day-hold_1d
idea: 060-02.d3_volume-growth-ten-day-hold
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of (forecast/10) x excess 10-bar return per day-case: 0.0829213; t of the mean over day-cases: 1.86511 (threshold: t >= 2 confirms (with rank correlation > 0), t <= -2 rejects, on >= 30 day-cases)
- Supporting check: Spearman rank correlation forecast vs excess 10-bar return > 0: 0.164695, passed: True
- Counts: day-cases: 147, cells: 447
- Decided by: The t lies between -2 and 2 on at least 30 day-cases, so the plan calls it inconclusive.
- Reading: The situation is checked as the 20-day close return below 0 (from prices, or the recorded 'mean_reversion' regime where the window holds fewer than 20 earlier bars), the falling profile being left to the code as the Fidelity says, and the expected side as the sign of the recorded raw 30/30-day log volume ratio; the coin's mean 10-bar return is taken over all its grid cells in all windows, and the main measure is the mean over day-cases of the per-date summed cell values, with the ordinary t of that mean.
- Size: unusual move +2.35 % (t 3.45, the cases of one day together: 410 days) per case over 10 bars, 0.156 of the coin's usual move (14.49 %); normal drift in its direction -0.19 %, total +2.16 %; 562 cases
Plan: `steps_cards/03_test_plan/night8_fallingcalm_run/plans/060-02.d3_volume-growth-ten-day-hold_1d.md`
Record: `steps_cards/04_backtest/night8_fallingcalm_run/backtests/060-02.d3_volume-growth-ten-day-hold_1d`
Measure: `measure.py`
