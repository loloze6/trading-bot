---
plan: 017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d2_settlement-fall-recovers-after-runup.b1_settlement-fall-recovery-more-coins_1h
idea: 017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d2_settlement-fall-recovers-after-runup.b1_settlement-fall-recovery-more-coins
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: forecast-weighted mean excess 24-bar return: 0.00153556; t of the weighted mean: 3.05311 (threshold: above 0 with t >= 2 to confirm (with correlation > 0); below 0 with t <= -2 to reject)
- Supporting check: Pearson correlation of case forecast and excess return: 0.0154859, passed: True
- Counts: cases: 12061
- Decided by: The forecast-weighted mean excess return is above 0 with t >= 2 and the correlation is above 0.
- Reading: Cases are holding-period bets (forecast rise of >= 2 points from its lowest level on its side since the last bet, from 0 after a flat), the first per 24-bar grid cell from each window's first row, dropped when the 24-bar return leaves the window; the weighted-mean t is the ordinary t of f_i*x_i/mean(f) over cases.
- Size: unusual move +0.12 % per case over 24 bars, 0.024 of the coin's usual move (5.50 %); normal drift in its direction +0.18 %, total +0.30 %; 12061 cases
Plan: `steps_cards/03_test_plan/retest_settlement_run/plans/017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d2_settlement-fall-recovers-after-runup.b1_settlement-fall-recovery-more-coins_1h.md`
Record: `steps_cards/04_backtest/retest_settlement_run/backtests/017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d2_settlement-fall-recovers-after-runup.b1_settlement-fall-recovery-more-coins_1h`
Measure: `measure.py`
