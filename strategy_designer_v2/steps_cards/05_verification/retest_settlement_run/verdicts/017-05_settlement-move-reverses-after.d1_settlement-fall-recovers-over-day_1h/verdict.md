---
plan: 017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day_1h
idea: 017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day
fit: exact
status: confirmed
---
Situation check: 99 % of the active bars match the plan's situation and side
Evidence:
- Main measure: forecast-weighted mean 24-bar excess return over normal drift: 0.00170132; t of weighted mean: 2.88492 (threshold: confirm: weighted mean > 0 with t >= 2 and supporting check passes; reject: weighted mean < 0 with t <= -2)
- Supporting check: top-half minus bottom-half forecast mean excess return: 0.00314255, passed: True
- Counts: independent cases: 12648
- Decided by: Weighted mean excess return above 0 with t >= 2 and the top-minus-bottom half check above 0.
- Reading: Settlement bars are those stamped 23:00 or 15:00 UTC (the next bar opens at 00:00 or 16:00) and a fall is a negative fall2h raw value (2-bar price return when not recorded); a case is the first settlement bar with forecast > 0 in each 24-bar grid cell of a window, with a full 24-bar forward return; the t of the forecast-weighted mean uses the weighted (sandwich) standard error with n/(n-1) correction; top and bottom halves are the upper and lower n//2 cases sorted by forecast (the middle case dropped if n is odd), compared on unweighted mean excess returns; the plan's 100-case minimum gives 'not observable'.
- Size: unusual move +0.09 % per case over 24 bars, 0.018 of the coin's usual move (4.87 %); normal drift in its direction +0.14 %, total +0.23 %; 11281 cases
Plan: `steps_cards/03_test_plan/retest_settlement_run/plans/017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day_1h.md`
Record: `steps_cards/04_backtest/retest_settlement_run/backtests/017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day_1h`
Measure: `measure.py`
