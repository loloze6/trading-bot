---
plan: 024-02_fading-volume-downrun-rebound-size.b1_extreme-down-streak-rebound-only.b1_deep-fading-down-streak-rebound_4h
idea: 024-02_fading-volume-downrun-rebound-size.b1_extreme-down-streak-rebound-only.b1_deep-fading-down-streak-rebound
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 18-bar excess return (return minus the coin's normal 18-bar drift) over bet cases: 0.000490671; t of the mean: 0.373915 (threshold: confirm: mean > 0 with t >= 2 on >= 30 cases and correlation > 0; reject: mean < 0 with t <= -2 on >= 30 cases)
- Supporting check: correlation of forecast at signal bar with 18-bar excess return: 0.0576957, passed: True
- Counts: cases: 4039
- Decided by: The t-statistic of the mean excess return lies between -2 and 2 (or is undefined), which the plan calls inconclusive.
- Reading: Down-streak = consecutive closes below the previous close inside the window, volume slope = OLS slope of the streak's down bars' volumes; a bet is a rise of the forecast of >= 2 points above its lowest long level since the last bet (reset to 0 when flat), the first bet of each 18-bar grid cell (from the window's first row) is the case, cases without 18 bars ahead in the window are dropped, and the drift is the coin's mean return over non-overlapping 18-bar grid stretches of all its windows.
- Size: unusual move +0.05 % per case over 18 bars, 0.007 of the coin's usual move (8.17 %); normal drift in its direction +0.41 %, total +0.46 %; 4039 cases
Plan: `steps_cards/03_test_plan/night4_exhaustion_run/plans/024-02_fading-volume-downrun-rebound-size.b1_extreme-down-streak-rebound-only.b1_deep-fading-down-streak-rebound_4h.md`
Record: `steps_cards/04_backtest/night4_exhaustion_run/backtests/024-02_fading-volume-downrun-rebound-size.b1_extreme-down-streak-rebound-only.b1_deep-fading-down-streak-rebound_4h`
Measure: `measure.py`
