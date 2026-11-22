---
plan: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins_1d
idea: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of drift-adjusted 5-bar forward return on forecast/10: 0.00313708; OLS slope t: 1.85562 (threshold: confirm at t >= 2 (with supporting mean > 0), reject at t <= -2)
- Supporting check: mean unusual 5-bar move in the forecast's direction: 0.00712313, passed: True
- Counts: grid cases in the regime: 3120
- Decided by: The slope's t is strictly between -2 and 2.
- Reading: Situation recomputed as |close[t]-close[t-30]| over the high-low range of the last 30 or 31 bars (either accepted), using the recorded regime where a window's early bars cannot be recomputed, with the expected side the sign of the 30-day return; the coin's drift is the mean 5-bar return over all grid bars of all its windows; the slope t is the ordinary OLS t with an intercept; and the plan's 'fewer than 100 grid cases' rule is applied as a minimum count giving 'not observable'.
- Size: unusual move +1.01 % per case over 5 bars, 0.074 of the coin's usual move (12.35 %); normal drift in its direction -0.07 %, total +0.94 %; 3153 cases
Plan: `steps_cards/03_test_plan/night4_range_run/plans/023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins_1d.md`
Record: `steps_cards/04_backtest/night4_range_run/backtests/023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins_1d`
Measure: `measure.py`
