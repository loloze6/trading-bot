---
plan: 017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses.b2_two-hour-settlement-snapback_1h
idea: 017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses.b2_two-hour-settlement-snapback
fit: exact
status: confirmed
---
Situation check: 99 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of mean of forecast/10 x excess 2-bar return on regime cases: 0.000749357; t of the mean: 6.70734 (threshold: confirm: mean > 0 with t >= 2 over >= 200 cases and correlation > 0; reject: mean < 0 with t <= -2 over >= 200 cases)
- Supporting check: Pearson correlation of forecast with excess 2-bar return: 0.0490917, passed: True
- Counts: cases: 21229, active bars: 21291
- Decided by: The mean is positive with t >= 2 over at least 200 cases and the correlation is above 0.
- Reading: Cases are all regime mean_reversion bars with non-zero forecast and a 2-bar forward close inside the window, each counted once, with the coin's mean 2-bar return taken on a non-overlapping grid (positions 0,2,4,...) pooled over all its windows; settlement bars are those whose next bar starts at 00/08/16 UTC.
- Size: unusual move +0.06 % per case over 2 bars, 0.044 of the coin's usual move (1.47 %); normal drift in its direction +0.00 %, total +0.06 %; 17766 cases
Plan: `steps_cards/03_test_plan/retest_settlement_run/plans/017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses.b2_two-hour-settlement-snapback_1h.md`
Record: `steps_cards/04_backtest/retest_settlement_run/backtests/017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses.b2_two-hour-settlement-snapback_1h`
Measure: `measure.py`
