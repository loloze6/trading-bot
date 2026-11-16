---
plan: 002-01_sma-golden-cross-upward-drift.b2_fresh-golden-cross-fades_1d
idea: 002-01_sma-golden-cross-upward-drift.b2_fresh-golden-cross-fades
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 10-bar forward excess return on regime bars vs coin's all-window grid mean: -0.0188103; t of the mean: -1.71286 (threshold: confirm if t <= -2 (with fresh-minus-stale below zero); reject if t >= +2; otherwise inconclusive)
- Supporting check: fresh (age 1-15) minus stale (age 16-30) excess return, Welch t below 0: 0.35656, passed: False
- Counts: non-overlapping regime cases: 166, fresh cases (age 1-15): 88, stale cases (age 16-30): 78
- Decided by: The main-measure t lies between -2 and +2.
- Reading: Regime bars and freshness are read from the raw cross_age value on grid bars (positions 0,10,20,... of each window, with the forward return inside the window), the baseline is each coin's mean 10-bar grid return over all its windows, the supporting check counts as passed only when the Welch t (fresh minus stale) is below 0, and fewer than 20 cases gives 'not observable' as the workflow's minimum-count rule requires.
Plan: `steps_cards/03_test_plan/plans/002-01_sma-golden-cross-upward-drift.b2_fresh-golden-cross-fades_1d.md`
Record: `steps_cards/04_backtest/backtests/002-01_sma-golden-cross-upward-drift.b2_fresh-golden-cross-fades_1d`
Measure: `measure.py`
