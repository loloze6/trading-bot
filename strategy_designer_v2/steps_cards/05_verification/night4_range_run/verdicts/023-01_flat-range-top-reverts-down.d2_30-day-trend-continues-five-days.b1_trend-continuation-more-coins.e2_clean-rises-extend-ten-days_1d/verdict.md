---
plan: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.e2_clean-rises-extend-ten-days_1d
idea: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.e2_clean-rises-extend-ten-days
fit: adapted
status: confirmed
---
Situation check: 99 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 10-bar excess return of rise-sized long bets over the coin's normal 10-bar drift: 0.0168371; t of the mean: 2.69334 (threshold: confirm: mean > 0 with t >= 2 over >= 30 cases and supporting check > 0; reject: mean < 0 with t <= -2 over >= 30 cases)
- Supporting check: mean excess above median forecast minus below median: 0.00581632, passed: True
- Counts: cases: 1095
- Decided by: Mean excess return positive with t >= 2 over at least 30 cases and the supporting check above 0.
- Reading: Situation = recomputed NMR (|close[t]-close[t-30]| over the high-low range of bars t-30..t) >= 0.5 (regime column where history is short) with a positive 30-day rise, long side; a case is the first long bet (forecast rise >= 2 from its lowest level since the last bet, reset to 0 when flat) in each 10-bar grid cell counted from each window's first row; the drift is the coin's mean non-overlapping 10-bar return pooled over its windows; the median split uses cases strictly above and strictly below the median forecast.
- Size: unusual move +1.68 % per case over 10 bars, 0.093 of the coin's usual move (16.82 %); normal drift in its direction +1.49 %, total +3.17 %; 1095 cases
Plan: `steps_cards/03_test_plan/night4_range_run/plans/023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.e2_clean-rises-extend-ten-days_1d.md`
Record: `steps_cards/04_backtest/night4_range_run/backtests/023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.e2_clean-rises-extend-ten-days_1d`
Measure: `measure.py`
