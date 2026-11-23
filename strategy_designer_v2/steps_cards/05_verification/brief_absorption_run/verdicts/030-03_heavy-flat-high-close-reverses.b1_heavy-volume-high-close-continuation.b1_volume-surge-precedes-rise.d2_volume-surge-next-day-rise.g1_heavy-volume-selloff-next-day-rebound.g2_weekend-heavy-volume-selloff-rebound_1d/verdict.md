---
plan: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.g1_heavy-volume-selloff-next-day-rebound.g2_weekend-heavy-volume-selloff-rebound_1d
idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.g1_heavy-volume-selloff-next-day-rebound.g2_weekend-heavy-volume-selloff-rebound
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: weekend-regime slope of next-day excess return on forecast: 0.000279503; OLS slope t: 1.9371 (threshold: confirm t >= 2 (with difference t >= 2); reject t <= -2)
- Supporting check: weekend slope minus weekday slope (Welch-style t): -0.000106006, passed: False
- Counts: weekend cases with forecast > 0: 2294, weekday cases with forecast > 0: 6220
- Decided by: inconclusive rule: weekend slope t 1.94 and difference t -0.63 meet neither the confirm nor the reject rule
- Reading: Situation bars are those whose recorded raw fall-times-volume value is above 0 with the regime matching the bar's own day (mean_reversion on Saturday/Sunday bars, unknown otherwise), expected side long; the regressions pool all coins and windows with every bar as a 1-bar case, the coin's mean daily return taken over all its windows, and the difference t is (b_we - b_wd)/sqrt(se_we^2 + se_wd^2).
- Size: unusual move +0.15 % per case over 1 bars, 0.033 of the coin's usual move (4.78 %); normal drift in its direction +0.12 %, total +0.27 %; 5314 cases
Plan: `steps_cards/03_test_plan/brief_absorption_run/plans/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.g1_heavy-volume-selloff-next-day-rebound.g2_weekend-heavy-volume-selloff-rebound_1d.md`
Record: `steps_cards/04_backtest/brief_absorption_run/backtests/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.g1_heavy-volume-selloff-next-day-rebound.g2_weekend-heavy-volume-selloff-rebound_1d`
Measure: `measure.py`
