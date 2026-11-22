---
plan: 023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues_1d
idea: 023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues
fit: exact
status: inconclusive
---
Situation check: 91 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of next-5-bar return minus coin drift on forecast, mean_reversion grid bars: -1.06379e-05; OLS slope t: -0.0215345 (threshold: confirm if slope t >= 2 and check passes; reject if slope t <= -2; inconclusive otherwise)
- Supporting check: mean next-5-bar return minus drift, short direction, forecast <= -2 grid bars: 0.00753876, passed: True
- Counts: grid bars with forecast < 0: 793, mean_reversion grid bars: 1085, cases (grid bars with forecast <= -2): 698
- Decided by: The slope's t is between -2 and 2.
- Reading: Situation computed from prices as |close[t]-close[t-29]| / (30-bar max high - min low) <= 0.5 and close < 30-bar high-low midpoint, with the 10-bar fall from fall10's raw value (prices when missing), active bars lacking 30 bars of in-window history left out of the agreement; drift is the coin's mean 5-bar return on the 0,5,10,... grid of all its windows; the regression pools all coins and windows with an intercept; the minimum count is the grid bars with forecast < 0 and a valid next-5-bar return.
- Size: unusual move +0.55 % per case over 5 bars, 0.046 of the coin's usual move (10.60 %); normal drift in its direction -0.58 %, total -0.04 %; 1170 cases
Plan: `steps_cards/03_test_plan/night4_range_run/plans/023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues_1d.md`
Record: `steps_cards/04_backtest/night4_range_run/backtests/023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues_1d`
Measure: `measure.py`
