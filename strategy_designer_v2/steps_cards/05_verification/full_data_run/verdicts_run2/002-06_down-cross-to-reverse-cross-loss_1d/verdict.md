---
plan: 002-06_down-cross-to-reverse-cross-loss_1d
idea: 002-06_down-cross-to-reverse-cross-loss
fit: adapted
status: inconclusive
---
Situation check: 1 of the active bars match the plan's situation and side
Evidence:
- Main measure: |forecast|-weighted mean excess short 1-bar return vs coin all-window mean: 6.57232e-05; t of the weighted mean: 0.116595 (threshold: above 0 with t >= 2 confirms; below 0 with t <= -2 rejects; otherwise inconclusive)
- Supporting check: share of short bars with next return below coin all-window mean (binomial z vs 50%): 0.512362, passed: True
- Counts: pooled bars with forecast below 0: 8453
- Decided by: Inconclusive: the t-statistic lies between -2 and 2.
- Reading: The coin's mean is the mean of all within-window next-bar returns pooled over all its windows, every bar with forecast below 0 and a next-bar return counts once, the t of the weighted mean uses the weighted standard error sqrt(sum w^2 (x - m)^2) / sum w with an n/(n-1) correction, and the supporting check counts as passed when the binomial z is at least 2 (it does not enter the decision).
Plan: `steps_cards/03_test_plan/full_data_run/plans/002-06_down-cross-to-reverse-cross-loss_1d.md`
Record: `steps_cards/04_backtest/full_data_run/backtests/002-06_down-cross-to-reverse-cross-loss_1d`
Measure: `measure.py`
