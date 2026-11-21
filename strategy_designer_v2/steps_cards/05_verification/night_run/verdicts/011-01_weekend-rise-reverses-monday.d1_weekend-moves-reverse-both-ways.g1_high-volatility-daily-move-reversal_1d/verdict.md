---
plan: 011-01_weekend-rise-reverses-monday.d1_weekend-moves-reverse-both-ways.g1_high-volatility-daily-move-reversal_1d
idea: 011-01_weekend-rise-reverses-monday.d1_weekend-moves-reverse-both-ways.g1_high-volatility-daily-move-reversal
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of allocation x (next-bar return - coin mean daily return) on mean_reversion bars: 0.00128714; ordinary t of the mean: 4.75586 (threshold: confirm: t >= 2 with positive mean; reject: t <= -2)
- Supporting check: down-day minus up-day mean reversal return (Welch t): 0.00150711, passed: False
- Counts: active bars: 8146, down-day bars: 3922, up-day bars: 4149
- Decided by: Inconclusive rule: main measure confirms but the down-minus-up check does not reach Welch t >= 2 with a positive difference nor t <= -2.
- Reading: Active bars are the mean_reversion-regime bars with a next close in the same window and a recorded allocation, down/up days are those with close[t]/close[t-1]-1 below/above zero inside the window (zero-return and window-first bars excluded), the coin mean is over all within-window daily returns, and the plan's 'below minimum, inconclusive' is reported as 'not observable' per the workflow.
- Size: unusual move +0.37 % per case over 1 bars, 0.079 of the coin's usual move (4.78 %); normal drift in its direction -0.00 %, total +0.37 %; 5316 cases
Plan: `steps_cards/03_test_plan/night_run/plans/011-01_weekend-rise-reverses-monday.d1_weekend-moves-reverse-both-ways.g1_high-volatility-daily-move-reversal_1d.md`
Record: `steps_cards/04_backtest/night_run/backtests/011-01_weekend-rise-reverses-monday.d1_weekend-moves-reverse-both-ways.g1_high-volatility-daily-move-reversal_1d`
Measure: `measure.py`
