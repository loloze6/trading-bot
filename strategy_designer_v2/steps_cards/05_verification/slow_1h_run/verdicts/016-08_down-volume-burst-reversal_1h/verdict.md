---
plan: 016-08_down-volume-burst-reversal_1h
idea: 016-08_down-volume-burst-reversal
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: top-half minus bottom-half mean excess 72-bar forward return (mean_reversion grid bars, split at forecast median): 0.00330914; Welch t: 1.04929 (threshold: confirm: difference > 0 with Welch t >= 2; reject: difference < 0 with Welch t <= -2; otherwise inconclusive)
- Supporting check: none
- Counts: grid cases in top half: 1381, grid cases in bottom half: 1381, active bars: 199840
- Decided by: The Welch t lies between -2 and 2 (inconclusive rule).
- Reading: The 72-bar return is recomputed as close[t]/close[t-72]-1 inside each window, so the first 72 bars of each window are left out of the situation check; grid bars are kept on the recorded regime 'mean_reversion'; the coin's mean 72-bar return is the mean of its non-overlapping grid returns over all windows; the median of forecast is taken over all kept grid bars of all coins pooled; and the plan's 'fewer than 30 grid cases in either half' minimum gives 'not observable'.
- Size: unusual move -0.44 % per case over 72 bars, -0.053 of the coin's usual move (8.23 %); normal drift in its direction +0.41 %, total -0.03 %; 4677 cases
Plan: `steps_cards/03_test_plan/slow_1h_run/plans/016-08_down-volume-burst-reversal_1h.md`
Record: `steps_cards/04_backtest/slow_1h_run/backtests/016-08_down-volume-burst-reversal_1h`
Measure: `measure.py`
