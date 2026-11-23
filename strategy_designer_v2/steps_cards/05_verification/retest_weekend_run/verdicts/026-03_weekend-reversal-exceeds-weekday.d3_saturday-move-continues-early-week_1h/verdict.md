---
plan: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week_1h
idea: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week
fit: exact
status: confirmed
---
Situation check: 99 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of 48-bar excess return on forecast, pooled: 0.000787881; OLS slope t: 4.56923 (threshold: confirm: slope > 0 with t >= 2 and supporting mean > 0; reject: slope < 0 with t <= -2)
- Supporting check: mean of sign(forecast) x (48-bar return - coin mean 48-bar return): 0.00480034, passed: True
- Counts: cases: 1864, cases_BTCUSD: 278, cases_ETHUSD: 312, cases_LTCUSD: 321, cases_XMRUSD: 338, cases_XRPUSD: 306, cases_ZECUSD: 309
- Decided by: The slope is positive with t >= 2 and the supporting mean is above 0 (confirm rule).
- Reading: Situation bars are those whose next bar starts Monday 00:00 UTC, with the expected side from the sign of the recorded raw Saturday return (prices at Saturday/Friday 23:00 bars when missing); 48-bar returns are by row position within a window, the coin's mean 48-bar return is taken on the non-overlapping grid 0, 48, 96, ... of all its windows, cases are trending bars with |forecast| >= 2 and a full 48-bar return in the window, and the slope's t is the ordinary OLS t.
- Size: unusual move +0.47 % per case over 48 bars, 0.078 of the coin's usual move (6.56 %); normal drift in its direction +0.03 %, total +0.51 %; 1856 cases
Plan: `steps_cards/03_test_plan/retest_weekend_run/plans/026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week_1h.md`
Record: `steps_cards/04_backtest/retest_weekend_run/backtests/026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week_1h`
Measure: `measure.py`
