---
plan: 032-02.g1.e1.e2_quiet-breakout-to-28-day-high_1d
idea: 032-02.g1.e1.e2_quiet-breakout-to-28-day-high
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of the slope of 5-bar excess return on the forecast, trending grid cases: 1.47238; OLS slope t: 1.47238 (threshold: confirm: t >= 2 with top-third minus bottom-third > 0; reject: t <= -2; under 100 grid cases: not observable)
- Supporting check: mean excess 5-bar return, top third of forecasts minus bottom third: 0.0190551, passed: True
- Counts: grid cases: 327, top third cases: 109, bottom third cases: 109
- Decided by: The slope's t is between -2 and 2: inconclusive.
- Reading: The situation is recomputed from closes as close equal to the 28-bar closing high inside each window (on a window's first 27 bars, the high of the bars available), its side per bar is long when the 20-to-60-day volatility ratio (recorded raw value, else recomputed from closes) is below 1 and short when above, since the Fidelity keeps the graded comparison; the cases are regime 'trending' bars at positions 0, 5, 10, ... of each window with a 5-bar forward close in the same window, the drift is the coin's mean 5-bar return on that grid over all windows, the regression is OLS with an intercept, and the thirds are the floor(n/3) largest and smallest forecasts.
- Size: unusual move +0.18 % (t 0.34, the cases of one day together: 494 days) per case over 5 bars, 0.026 of the coin's usual move (10.60 %); normal drift in its direction +0.06 %, total +0.24 %; 711 cases
Plan: `steps_cards/03_test_plan/night7c_steadydecline_run/plans/032-02.g1.e1.e2_quiet-breakout-to-28-day-high_1d.md`
Record: `steps_cards/04_backtest/night7c_steadydecline_run/backtests/032-02.g1.e1.e2_quiet-breakout-to-28-day-high_1d`
Measure: `measure.py`
