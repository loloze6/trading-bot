---
plan: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.g1_volatility-scaled-fall-next-day-rebound_1d
idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.g1_volatility-scaled-fall-next-day-rebound
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: forecast-weighted mean next-day excess return on bars with forecast > 0: 0.00427275; t of the weighted mean: 2.50338 (threshold: confirm: positive with t >= 2 and Spearman > 0; reject: negative with t <= -2)
- Supporting check: Spearman(forecast, next-day excess return) on forecast > 0 bars > 0: None, passed: None
- Counts: bars with forecast > 0: 1059
- Decided by: The weighted mean is positive with t >= 2 but the Spearman check fails.
- Reading: The t of the forecast-weighted mean uses the weighted standard error sqrt(sum(w^2 (x-m)^2) / (sum w)^2 * n/(n-1)), every in-window bar with a next bar counts as a case, the coin's mean daily return is over all its in-window daily returns, and the plan's 200-bar minimum yields 'not observable' when unmet.
- Size: unusual move +0.22 % per case over 1 bars, 0.044 of the coin's usual move (4.78 %); normal drift in its direction +0.12 %, total +0.34 %; 942 cases
Plan: `steps_cards/03_test_plan/book_reflects_idea_run/plans/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.g1_volatility-scaled-fall-next-day-rebound_1d.md`
Record: `steps_cards/04_backtest/book_reflects_idea_run/backtests/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.g1_volatility-scaled-fall-next-day-rebound_1d`
Measure: `measure.py`
