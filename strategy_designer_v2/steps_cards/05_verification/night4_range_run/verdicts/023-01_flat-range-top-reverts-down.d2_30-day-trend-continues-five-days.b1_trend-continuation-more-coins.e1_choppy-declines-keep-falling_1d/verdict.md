---
plan: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.e1_choppy-declines-keep-falling_1d
idea: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.e1_choppy-declines-keep-falling
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean drift-adjusted 5-bar move in the short direction: 0.00923143; t of the mean: 4.01444 (threshold: t >= 2 confirms, t <= -2 rejects, over at least 30 independent cases)
- Supporting check: slope of drift-adjusted 5-bar return on forecast (grid bars, forecast < 0): 0.000536543, passed: True
- Counts: independent cases: 2049, supporting grid bars: 1857
- Decided by: Mean unusual short move has t >= 2 over at least 30 cases and the supporting slope is positive.
- Reading: Situation = 30-bar close return < 0 computed inside each window (falling back to the recorded regime 'mean_reversion' on the first 30 bars, where it cannot be computed) with a short forecast; a case is the first bar in each 5-bar grid cell (positions 0,5,10,... of each window) where the short forecast's size rises by >= 2 points from its smallest size since the last bet (reset to 0 at each window start, flat or side change), cases with no 5-bar return inside the window are dropped, drift is the coin's mean grid 5-bar return over all its windows, and fewer than 30 cases is reported as 'not observable'.
- Size: unusual move +0.92 % per case over 5 bars, 0.071 of the coin's usual move (12.35 %); normal drift in its direction -0.80 %, total +0.13 %; 2049 cases
Plan: `steps_cards/03_test_plan/night4_range_run/plans/023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.e1_choppy-declines-keep-falling_1d.md`
Record: `steps_cards/04_backtest/night4_range_run/backtests/023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.e1_choppy-declines-keep-falling_1d`
Measure: `measure.py`
