---
plan: 074-01.b1.d3_agitated-falling-run-break-fade_1d
idea: 074-01.b1.d3_agitated-falling-run-break-fade
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean next-day short-signed excess return on nonzero-forecast bars: 0.0127161; t of the mean (cases summed per day): 2.84182 (threshold: confirm: mean > 0 with t >= 2 and slope > 0; reject: t <= -2)
- Supporting check: OLS slope of short-signed excess on |forecast|: 0.00104554, passed: True
- Counts: cases: 342, distinct days: 201
- Decided by: The mean short-signed excess return is above 0 with t >= 2 and the supporting slope is above 0.
- Reading: The run break is recomputed from in-window closes (up close after at least two down closes, falling back on a positive recorded run_depth raw value on the first three bars of a window) and the falling-agitated profile is read from the recorded regime being 'mean_reversion' since the 365-day volatility percentile cannot be rebuilt from ~120-bar windows; the main value is the mean per case, its t is the ordinary t of the per-day sums, and the slope is an OLS of per-case short-signed excess on absolute forecast.
- Size: unusual move +1.17 % (t 2.65, the cases of one day together: 196 days) per case over 1 bars, 0.238 of the coin's usual move (4.73 %); normal drift in its direction -0.13 %, total +1.04 %; 331 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.004901 on the check folds against +0.01272 on every fold
Plan: `steps_cards/03_test_plan/night9_fallcalmfade_run/plans/074-01.b1.d3_agitated-falling-run-break-fade_1d.md`
Record: `steps_cards/04_backtest/night9_fallcalmfade_run/backtests/074-01.b1.d3_agitated-falling-run-break-fade_1d`
Measure: `measure.py`
