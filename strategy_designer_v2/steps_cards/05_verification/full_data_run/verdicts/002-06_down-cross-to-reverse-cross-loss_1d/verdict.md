---
plan: 002-06_down-cross-to-reverse-cross-loss_1d
idea: 002-06_down-cross-to-reverse-cross-loss
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: |forecast|-weighted mean excess short 1-bar return (next return minus coin all-window mean, sign flipped), pooled: 6.57232e-05; t of the weighted mean: 0.116596 (threshold: confirm: mean > 0 with t >= 2; reject: mean < 0 with t <= -2; else inconclusive; fewer than 300 pooled bars with forecast < 0 is not observable)
- Supporting check: share of forecast<0 bars with next return below coin mean, binomial z vs 50%: 2.27322, passed: True
- Counts: pooled bars with forecast below 0: 8453, bars with next return below coin mean: 4331
- Decided by: The t-statistic of the weighted mean excess short return lies between -2 and 2.
- Reading: Situation taken as last_history_value of sma_cross_spread < 0 (50-day SMA below 200-day SMA) with forecast < 0 on active bars; the weighted mean is sum(-(r-mu)|f|)/sum(|f|) with its t the ordinary t of the values -(r-mu)|f|/mean|f| (each bar once, h=1); mu is the coin's mean next-bar return over all its windows; the 300-bar minimum counts bars with forecast < 0 and a valid next return; the supporting check passes when the share below the mean exceeds 50% with binomial z >= 2. (share below mean = 0.5124).
- Size: unusual move -0.13 % per case over 1 bars, -0.035 of the coin's usual move (4.73 %); normal drift in its direction -0.13 %, total -0.26 %; 373 cases
Plan: `steps_cards/03_test_plan/full_data_run/plans/002-06_down-cross-to-reverse-cross-loss_1d.md`
Record: `steps_cards/04_backtest/full_data_run/backtests/002-06_down-cross-to-reverse-cross-loss_1d`
Measure: `measure.py`
