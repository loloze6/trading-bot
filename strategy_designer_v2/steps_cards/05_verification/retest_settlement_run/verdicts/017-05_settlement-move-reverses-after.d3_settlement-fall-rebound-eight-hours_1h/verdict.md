---
plan: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours_1h
idea: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours
fit: exact
status: confirmed
---
Situation check: 99 % of the active bars match the plan's situation and side
Evidence:
- Main measure: forecast-weighted mean 8-bar excess return of settlement cases with forecast >= 2: 0.00187065; t of the weighted mean: 5.88766 (threshold: confirm: above 0 with t >= 2; reject: below 0 with t <= -2; otherwise inconclusive)
- Supporting check: upper-half minus lower-half mean excess return (median forecast split), Welch t 3.765: 0.00184233, passed: True
- Counts: cases across all coins and windows: 14329, upper half cases: 7164, lower half cases: 7165
- Decided by: The forecast-weighted mean excess return is above 0 with t >= 2 and the upper-minus-lower half difference is above 0.
- Reading: Settlement bars are those whose close (timestamp + 1h) is at 00:00 or 16:00 UTC and a fall is a negative raw fall2h value (2-bar price return where not recorded); cases are bars with regime mean_reversion and forecast >= 2, 8-bar returns by row position inside a window, the coin's normal drift is the mean of its non-overlapping 8-bar returns (positions 0, 8, 16, ...) over all its windows, the t of the weighted mean uses the robust standard error sqrt(n/(n-1)*sum(w^2 (x-m)^2))/sum(w), and the median split puts forecasts above the median in the upper half and the rest in the lower half.
- Size: unusual move +0.12 % per case over 8 bars, 0.043 of the coin's usual move (2.81 %); normal drift in its direction +0.05 %, total +0.17 %; 14278 cases
Plan: `steps_cards/03_test_plan/retest_settlement_run/plans/017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours_1h.md`
Record: `steps_cards/04_backtest/retest_settlement_run/backtests/017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours_1h`
Measure: `measure.py`
