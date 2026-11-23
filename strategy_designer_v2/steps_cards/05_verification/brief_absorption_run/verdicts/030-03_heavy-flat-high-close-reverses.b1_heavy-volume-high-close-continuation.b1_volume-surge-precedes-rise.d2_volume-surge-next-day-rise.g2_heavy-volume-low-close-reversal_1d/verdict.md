---
plan: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.g2_heavy-volume-low-close-reversal_1d
idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.g2_heavy-volume-low-close-reversal
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of pooled slope of excess next-day return on forecast (absorb post_pipeline_value): 6.22524; OLS slope t: 6.22524 (threshold: t >= 2 (with check difference > 0) confirms, t <= -2 rejects, between is inconclusive)
- Supporting check: slope on close location, volume ratio >= 1 minus ratio < 1: 0.00746806, passed: True
- Counts: bars with forecast > 2: 11443, regression bars: 17380, heavy-volume days (ratio >= 1): 5506, light-volume days (ratio < 1): 8994
- Decided by: The slope t is >= 2 and the supporting check's difference is > 0.
- Reading: Situation bars are those whose recorded raw absorb value (close-location x volume ratio, recomputed from prices where not recorded) is > 0, with the expected side long; the coin's mean daily return is the mean of all its in-window next-day returns pooled over windows; the supporting check's volume ratio is recomputed inside each window from the prior 20 recorded bars (first 20 bars of each window left out), ordinary OLS slopes are used, and 'bars with forecast > 2' counts the recorded forecast column.
- Size: unusual move +0.11 % per case over 1 bars, 0.025 of the coin's usual move (4.78 %); normal drift in its direction +0.12 %, total +0.23 %; 6298 cases
Plan: `steps_cards/03_test_plan/brief_absorption_run/plans/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.g2_heavy-volume-low-close-reversal_1d.md`
Record: `steps_cards/04_backtest/brief_absorption_run/backtests/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.g2_heavy-volume-low-close-reversal_1d`
Measure: `measure.py`
