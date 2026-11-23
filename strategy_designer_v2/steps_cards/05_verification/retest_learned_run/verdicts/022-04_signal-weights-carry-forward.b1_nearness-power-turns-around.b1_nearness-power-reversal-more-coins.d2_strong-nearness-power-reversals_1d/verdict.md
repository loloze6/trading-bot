---
plan: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals_1d
idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled slope of drift-removed 5-day return on forecast: 0.000287203; OLS t of slope: 2.01906 (threshold: confirm: slope > 0 with t >= 2 (and timing > 0); reject: slope < 0 with t <= -2)
- Supporting check: timing part of book's mean daily return before costs: 0.000381214, passed: True
- Counts: grid cases with a nonzero forecast: 4729, grid cases: 4732
- Decided by: The slope is positive with t >= 2 and the timing part of the book's mean daily return is above 0.
- Reading: Active bars are bars with a nonzero forecast and a recorded raw value, the expected side being the opposite of the raw (w - wbar) x z sign because of negate; the slope is the OLS slope (with intercept) of each grid case's 5-day return minus the coin's mean 5-day grid return over all its windows, on the forecast, pooled over all grid cases including zero forecasts; the timing part is the mean over days of the coins' mean gross daily gain (position after the previous bar's trade x the bar's return) minus the same with the coin's mean daily return over all windows; the plan's 'fewer than 300 grid cases with a nonzero forecast' is applied first as the minimum count.
- Size: unusual move +0.08 % per case over 5 bars, 0.007 of the coin's usual move (11.11 %); normal drift in its direction +0.01 %, total +0.09 %; 1763 cases
Plan: `steps_cards/03_test_plan/retest_learned_run/plans/022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals_1d.md`
Record: `steps_cards/04_backtest/retest_learned_run/backtests/022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals_1d`
Measure: `measure.py`
