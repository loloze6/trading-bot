---
plan: 017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses.b1_settlement-reversal-more-coins_1h
idea: 017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses.b1_settlement-reversal-more-coins
fit: exact
status: confirmed
---
Situation check: 98 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of forecast/10 x drift-adjusted 8-bar return over settlement mean_reversion cases: 0.000371917; t of the mean: 2.31148 (threshold: confirm: mean > 0 with t >= 2 and supporting difference > 0; reject: mean < 0 with t <= -2)
- Supporting check: top-half minus bottom-half |forecast| drift-adjusted 8-bar return in forecast direction: 0.000432817, passed: True
- Counts: cases: 44640, top half: 22320, bottom half: 22320
- Decided by: Main mean > 0 with t >= 2 and the top-half minus bottom-half difference > 0.
- Reading: Settlement bar = bar whose next bar (timestamp + 1h) starts at 00/08/16 UTC, 2- and 24-bar returns taken positionally inside each window, expected side = sign of the 24-bar return; cases with no 8-bar forward return in their window are left out; halves are the upper and lower floor(n/2) cases sorted by |forecast| (stable sort, middle case dropped when n is odd); fewer than 200 cases is reported as not observable per the workflow's minimum-count rule.
- Size: unusual move +0.01 % per case over 8 bars, 0.001 of the coin's usual move (3.12 %); normal drift in its direction -0.00 %, total +0.01 %; 37871 cases
Plan: `steps_cards/03_test_plan/retest_settlement_run/plans/017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses.b1_settlement-reversal-more-coins_1h.md`
Record: `steps_cards/04_backtest/retest_settlement_run/backtests/017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses.b1_settlement-reversal-more-coins_1h`
Measure: `measure.py`
