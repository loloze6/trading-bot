---
plan: N5-01_breakout-after-strong-month_1d
idea: N5-01_breakout-after-strong-month
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of 10-bar forward excess return on forecast (new-high bars): -0.00014394; Newey-West t (lag 9): -0.128643 (threshold: slope > 0 with Newey-West t >= 2 (confirm); slope < 0 with t <= -2 (reject))
- Supporting check: mean 10-bar excess return, top third minus bottom third of forecasts: -0.00138045, passed: False
- Counts: non-overlapping new-high events: 559, new-high bars: 1874
- Decided by: Slope t-stat between -2 and 2 (inconclusive rule).
- Reading: Situation = close above each of its prior 20 closes in the same window (regime == 'trending' used where fewer than 20 prior closes exist), expected side long; coin mean = mean of all 10-bar forward returns of that coin pooled over windows; Newey-West lag 9 applied to pairs of new-high bars of the same coin-window at most 9 bars apart (Bartlett weights); thirds by forecast quantiles 1/3 and 2/3; non-overlapping events counted greedily per coin-window, an event at least 10 bars after the previous counted one.
Plan: `steps_cards/03_test_plan/overnight_run/plans/N5-01_breakout-after-strong-month_1d.md`
Record: `steps_cards/04_backtest/overnight_run/backtests/N5-01_breakout-after-strong-month_1d`
Measure: `measure.py`
