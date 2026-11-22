---
plan: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.e2_clean-rises-extend-ten-days_1d
idea: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.e2_clean-rises-extend-ten-days
fit: adapted
status: inconclusive
---
Situation check: 98 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 10-bar excess return of rise-sized long bets over the coin's normal 10-bar drift: 0.00739287; t of the mean: 0.725559 (threshold: confirm: mean > 0 with t >= 2 over >= 30 cases and supporting check > 0; reject: mean < 0 with t <= -2 over >= 30 cases)
- Supporting check: mean excess above median forecast minus below median: 0.0327097, passed: True
- Counts: cases: 175
- Decided by: t between -2 and 2 (or undefined), which the plan calls inconclusive.
- Reading: Situation = recomputed NMR (|close[t]-close[t-30]| over the high-low range of bars t-30..t) >= 0.5 (regime column where history is short) with a positive 30-day rise, long side; a case is the first long bet (forecast rise >= 2 from its lowest level since the last bet, reset to 0 when flat) in each 10-bar grid cell counted from each window's first row; the drift is the coin's mean non-overlapping 10-bar return pooled over its windows; the median split uses cases strictly above and strictly below the median forecast.
- Size: unusual move +0.74 % per case over 10 bars, 0.072 of the coin's usual move (11.10 %); normal drift in its direction +0.48 %, total +1.22 %; 175 cases
Plan: `steps_cards/03_test_plan/night4_range_run/plans/023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.e2_clean-rises-extend-ten-days_1d.md`
Record: `steps_cards/04_backtest/night4_range_run/unseen_2026/backtests/023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.e2_clean-rises-extend-ten-days_1d`
Measure: `measure.py`
