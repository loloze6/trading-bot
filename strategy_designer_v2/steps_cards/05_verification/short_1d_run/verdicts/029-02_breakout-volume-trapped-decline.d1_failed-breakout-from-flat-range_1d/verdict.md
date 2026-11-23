---
plan: 029-02_breakout-volume-trapped-decline.d1_failed-breakout-from-flat-range_1d
idea: 029-02_breakout-volume-trapped-decline.d1_failed-breakout-from-flat-range
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-direction 5-bar unusual move (return minus coin drift) over short bets, pooled: -0.00355834; t of the mean: -0.84818 (threshold: confirm t >= 2 on at least 30 independent cases; reject t <= -2)
- Supporting check: t of LS slope of unusual move on pre-breakout 20-day return (slope -0.0235122): -1.48806, passed: False
- Counts: independent cases: 641, cases with pre-breakout return: 528
- Decided by: Neither confirm nor reject is met (main t between -2 and 2, or a confirmed fall with slope t between -2 and 2 or not computable): inconclusive.
- Reading: Cases are the first short-side bet (forecast rise of >= 2 points from its lowest short level since the last bet) in each 5-bar grid cell of each window, with a full 5-bar forward return inside the window; the breakout bar j is the most recent of the 1-3 prior bars closing above its prior 20 closes, cases without close[j-21] in the window are left out of the slope, and the situation on bars lacking 20+3 bars of window history is read from the recorded raw value being above 0.
- Size: unusual move -0.36 % per case over 5 bars, -0.027 of the coin's usual move (10.60 %); normal drift in its direction -0.58 %, total -0.93 %; 641 cases
Plan: `steps_cards/03_test_plan/short_1d_run/plans/029-02_breakout-volume-trapped-decline.d1_failed-breakout-from-flat-range_1d.md`
Record: `steps_cards/04_backtest/short_1d_run/backtests/029-02_breakout-volume-trapped-decline.d1_failed-breakout-from-flat-range_1d`
Measure: `measure.py`
