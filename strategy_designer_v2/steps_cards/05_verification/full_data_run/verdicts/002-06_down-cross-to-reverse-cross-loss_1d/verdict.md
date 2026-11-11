---
plan: 002-06_down-cross-to-reverse-cross-loss_1d
idea: 002-06_down-cross-to-reverse-cross-loss
fit: adapted
status: inconclusive
---
Situation check: 1 of the active bars match the plan's situation and side
Evidence:
- Main measure: |forecast|-weighted mean excess short 1-bar return vs coin all-window mean: 6.57232e-05; t of weighted mean (heteroskedasticity-robust weighted SE): 0.116595 (threshold: confirm if weighted mean excess short return > 0 with t >= 2; reject if < 0 with t <= -2; otherwise, or with fewer than 300 pooled forecast<0 bars, inconclusive)
- Supporting check: share of forecast<0 bars with next return below coin mean (binomial z vs 50%): 0.512362, passed: True
- Counts: pooled bars with forecast below 0: 8453
- Decided by: Inconclusive: the t-statistic lies between -2 and 2.
- Reading: The situation is a raw spread below 0 with a negative forecast; the coin's mean is the mean of all its within-window next-bar returns over all its windows; the weighted mean's t uses the robust weighted standard error sqrt(sum w^2 (x-m)^2)/sum w with n/(n-1) correction; the supporting check passes when its binomial z is at least 2 (z = 2.2732).
Plan: `steps_cards/03_test_plan/full_data_run/plans/002-06_down-cross-to-reverse-cross-loss_1d.md`
Record: `steps_cards/04_backtest/full_data_run/backtests/002-06_down-cross-to-reverse-cross-loss_1d`
Measure: `measure.py`
