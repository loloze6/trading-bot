---
plan: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day.d1_absorption-rebound-in-stressed-markets_1d
idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day.d1_absorption-rebound-in-stressed-markets
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: forecast-weighted mean next-day excess return: 0.00404715; t of the weighted mean over cases: 5.00148 (threshold: confirm: above 0 with t >= 2 and supporting check passes; reject: below 0 with t <= -2)
- Supporting check: top-third minus bottom-third mean excess return: 0.00616661, passed: True
- Counts: cases with forecast > 0: 8514
- Decided by: The weighted mean excess return is above 0 with t >= 2 and the top-third minus bottom-third difference is above 0.
- Reading: The situation holds on bars where the component's raw value (fall x volume ratio x volatility ratio) is above 0, falling back to a price fall when it is missing, on the long side; the t of the weighted mean is the ordinary t of the per-case values forecast x excess / mean forecast; the top and bottom thirds are the n//3 cases with the highest and lowest forecast; the 300-case minimum gives 'not observable'.
- Size: unusual move +0.15 % per case over 1 bars, 0.032 of the coin's usual move (4.78 %); normal drift in its direction +0.12 %, total +0.27 %; 4985 cases
Plan: `steps_cards/03_test_plan/brief_absorption_run/plans/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day.d1_absorption-rebound-in-stressed-markets_1d.md`
Record: `steps_cards/04_backtest/brief_absorption_run/backtests/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day.d1_absorption-rebound-in-stressed-markets_1d`
Measure: `measure.py`
