---
plan: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d1_strong-settlement-fall-day-rebound.b1_settlement-fall-rebound-more-coins_1h
idea: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d1_strong-settlement-fall-day-rebound.b1_settlement-fall-rebound-more-coins
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 24-bar move of settlement bets (forecast >= 2): 0.000746623; t of the mean: 1.57853 (threshold: confirm: mean > 0 with t >= 2 and supporting difference > 0; reject: mean < 0 with t <= -2; at least 30 independent cases)
- Supporting check: Welch difference of mean unusual move, cases minus small falls (0 < forecast < 2): 0.00136067, passed: True
- Counts: independent cases: 13768, small-fall settlement bars: 17227
- Decided by: the t of the cases' mean unusual move lies between -2 and 2.
- Reading: settlement bars are bars whose end (start + 1 h) is 00:00 or 16:00 UTC; cases and small falls are each kept as the first such bar per 24-bar grid cell counted from each window's first row, with the 24-bar forward return inside the window; the coin's mean 24-bar return is taken on the non-overlapping grid of all its windows; the supporting check passes when the difference is above 0; fewer than 30 cases is reported as not observable.
- Size: unusual move +0.08 % per case over 24 bars, 0.017 of the coin's usual move (5.50 %); normal drift in its direction +0.18 %, total +0.26 %; 13798 cases
Plan: `steps_cards/03_test_plan/retest_settlement_run/plans/017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d1_strong-settlement-fall-day-rebound.b1_settlement-fall-rebound-more-coins_1h.md`
Record: `steps_cards/04_backtest/retest_settlement_run/backtests/017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d1_strong-settlement-fall-day-rebound.b1_settlement-fall-rebound-more-coins_1h`
Measure: `measure.py`
