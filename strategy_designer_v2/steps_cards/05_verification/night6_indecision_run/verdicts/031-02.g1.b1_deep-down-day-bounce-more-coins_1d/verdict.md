---
plan: 031-02.g1.b1_deep-down-day-bounce-more-coins_1d
idea: 031-02.g1.b1_deep-down-day-bounce-more-coins
fit: adapted
status: mismatch
---
Situation check: 0 % of the active bars are bars of the plan's situation on its side (90 % needed).
- Decided by: Only 0.0% of the bars with a non-zero forecast are long bars on a day whose return ranks in the bottom 5 % of the coin's past daily returns, below the 90 % needed.
- Reading: The rank is recomputed from close-to-close returns inside each window over the past returns available (current included, share of returns at or above it >= 0.95), and where fewer than 20 past returns are visible the recorded regime plus a down day stands for it; the t is the case mean over a standard error with each day's deviations summed into one, and the mean daily return per coin is over all its windows.
Plan: `steps_cards/03_test_plan/night6_indecision_run/plans/031-02.g1.b1_deep-down-day-bounce-more-coins_1d.md`
Record: `steps_cards/04_backtest/night6_indecision_run/backtests/031-02.g1.b1_deep-down-day-bounce-more-coins_1d`
Measure: `measure.py`
