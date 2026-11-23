---
plan: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.g1_volatility-scaled-fall-next-day-rebound_1d
idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.g1_volatility-scaled-fall-next-day-rebound
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: forecast-weighted mean next-day excess return on bars with forecast > 0: 0.00315566; t of the weighted mean: 4.44309 (threshold: confirm: positive with t >= 2 and Spearman > 0; reject: negative with t <= -2)
- Supporting check: Spearman(forecast, next-day excess return) on forecast > 0 bars > 0: 0.0618227, passed: True
- Counts: bars with forecast > 0: 8514
- Decided by: The weighted mean excess return is positive with t >= 2 and the Spearman correlation is above 0.
- Reading: The t of the forecast-weighted mean uses the weighted standard error sqrt(sum(w^2 (x-m)^2) / (sum w)^2 * n/(n-1)), every in-window bar with a next bar counts as a case, the coin's mean daily return is over all its in-window daily returns, and the plan's 200-bar minimum yields 'not observable' when unmet.
- Size: unusual move +0.19 % per case over 1 bars, 0.039 of the coin's usual move (4.78 %); normal drift in its direction +0.12 %, total +0.31 %; 5665 cases
Plan: `steps_cards/03_test_plan/brief_absorption_run/plans/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.g1_volatility-scaled-fall-next-day-rebound_1d.md`
Record: `steps_cards/04_backtest/brief_absorption_run/backtests/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.g1_volatility-scaled-fall-next-day-rebound_1d`
Measure: `measure.py`
