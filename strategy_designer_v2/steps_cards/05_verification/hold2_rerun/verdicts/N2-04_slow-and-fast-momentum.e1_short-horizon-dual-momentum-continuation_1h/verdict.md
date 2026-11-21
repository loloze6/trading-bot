---
plan: N2-04_slow-and-fast-momentum.e1_short-horizon-dual-momentum-continuation_1h
idea: N2-04_slow-and-fast-momentum.e1_short-horizon-dual-momentum-continuation
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess 72-bar forward return over the coin's mean 72-bar return, at forecast > 0 grid bars: 0.00370984; t of the mean: 1.66123 (threshold: t >= 2 over at least 100 cases confirms; t <= -2 over at least 100 cases rejects)
- Supporting check: mean daily timing gain of the book over trending days: 0.00105449, passed: True
- Counts: non-overlapping in-situation cases: 1858, trending days in the timing check: 2050, active bars: 136850
- Decided by: The t of the mean excess 72-bar return lies between -2 and 2.
- Reading: Cases are the bars at positions 0, 72, 144, ... of each window with forecast > 0 and a close 72 bars later in the same window, the holding mean is the coin's mean 72-bar return over all grid bars of all its windows, and the timing check uses the days containing at least one trending bar, with the position held over the day taken as the mean allocation carried into each of the day's bars.
Plan: `steps_cards/03_test_plan/hold2_rerun/plans/N2-04_slow-and-fast-momentum.e1_short-horizon-dual-momentum-continuation_1h.md`
Record: `steps_cards/04_backtest/hold2_rerun/backtests/N2-04_slow-and-fast-momentum.e1_short-horizon-dual-momentum-continuation_1h`
Measure: `measure.py`
