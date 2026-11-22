---
plan: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days_1d
idea: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: Pearson correlation of forecast with next 5-bar return minus normal drift: 0.0336886; correlation t: 1.29413 (threshold: confirm: r > 0 with t >= 2 and timing part > 0; reject: r < 0 with t <= -2; at least 30 independent cases)
- Supporting check: book mean daily return before costs minus market-rise gain (timing part): 0.000626892, passed: True
- Counts: independent cases: 1476
- Decided by: The correlation's t is between -2 and 2, which the plan calls inconclusive.
- Reading: The situation is rebuilt as |close[t]-close[t-30]| over the max high minus min low of the last 30 bars (the recorded regime stands in where a window has under 30 bars of history) with the side the sign of the raw 30-bar return; the normal drift is each coin's mean 5-bar return on the non-overlapping grid of all its windows; 'before costs' is the position after each bar's trade times the next bar's return, averaged over coins per day, with the market part the same position times the coin's mean daily return.
- Size: unusual move +0.77 % per case over 5 bars, 0.065 of the coin's usual move (10.60 %); normal drift in its direction -0.03 %, total +0.73 %; 1483 cases
Plan: `steps_cards/03_test_plan/night4_range_run/plans/023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days_1d.md`
Record: `steps_cards/04_backtest/night4_range_run/backtests/023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days_1d`
Measure: `measure.py`
