---
plan: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d1_saturday-continuation-in-calm-markets_1h
idea: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d1_saturday-continuation-in-calm-markets
fit: exact
status: confirmed
---
Situation check: 97 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of (forecast/10) x de-drifted 48-bar return: 0.00723445; t of the mean: 4.13784 (threshold: confirm: mean > 0 with t >= 2 over at least 100 cases; reject: mean < 0 with t <= -2 over at least 100 cases)
- Supporting check: upper-half minus lower-half mean directional de-drifted return (split at median abs forecast): 0.00449914, passed: True
- Counts: cases: 1526
- Decided by: The main mean is positive with t >= 2 over at least 100 cases and the supporting check is positive.
- Reading: The situation bar is the bar whose start timestamp is Sunday 23:00 UTC, the calm-volatility gate is read from the recorded regime ('trending') because the detector's 8760-bar volatility ratio is not recorded and cannot be rebuilt inside a window, Saturday's move is close(Sun 00:00)/close(Sat 00:00)-1 by timestamp (sat_move raw value sign if a bar is missing); cases are pooled over all coins and windows, the drift is each coin's mean 48-bar return on the 0,48,96,... grid of all its windows, and the supporting split puts abs(forecast) above the median in the upper half and the rest in the lower half.
- Size: unusual move +0.61 % per case over 48 bars, 0.101 of the coin's usual move (6.56 %); normal drift in its direction +0.04 %, total +0.65 %; 1199 cases
Plan: `steps_cards/03_test_plan/retest_weekend_run/plans/026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d1_saturday-continuation-in-calm-markets_1h.md`
Record: `steps_cards/04_backtest/retest_weekend_run/backtests/026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d1_saturday-continuation-in-calm-markets_1h`
Measure: `measure.py`
