---
plan: 017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d2_settlement-fall-recovers-after-runup_1h
idea: 017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d2_settlement-fall-recovers-after-runup
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of (24-bar return minus coin mean 24-bar return) x forecast/10 on settlement-bar bets: 0.00338288; t of the mean: 3.1472 (threshold: confirm t >= 2 with supporting check passing on >= 100 cases; reject t <= -2 on >= 100 cases)
- Supporting check: mean excess 24-bar return, upper half minus lower half at the median forecast: None, passed: False
- Counts: cases: 5740
- Decided by: The main measure's t is 2 or more but the supporting check fails (upper half minus lower half not above 0).
- Reading: Settlement bars are those whose close (start + 1 hour) is at 00:00 or 16:00 UTC, a case is the first bet (forecast rise of at least 2) on a settlement bar in each 24-row grid cell of a window, the coin mean is over non-overlapping 24-bar returns at rows 0, 24, ... of all windows, and the upper half is forecasts strictly above the median, the lower half at or below it.
- Size: unusual move +0.18 % per case over 24 bars, 0.035 of the coin's usual move (4.87 %); normal drift in its direction +0.14 %, total +0.33 %; 5753 cases
Plan: `steps_cards/03_test_plan/retest_settlement_run/plans/017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d2_settlement-fall-recovers-after-runup_1h.md`
Record: `steps_cards/04_backtest/retest_settlement_run/backtests/017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d2_settlement-fall-recovers-after-runup_1h`
Measure: `measure.py`
