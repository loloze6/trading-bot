---
plan: 060-01.b1_falling-calm-high-close-fade_1d
idea: 060-01.b1_falling-calm-high-close-fade
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: next-day short-direction return minus the coin's mean daily return, over cases with forecast below 0: 0.00298976; t of the mean, cases grouped by day: 1.00175 (threshold: confirm: mean above 0 with day-grouped t >= 2 and check passes; reject: mean below 0 with t <= -2)
- Supporting check: upper-half minus lower-half excess return, split at median close location: 0.0058335, passed: True
- Counts: cases: 321, distinct days: 186
- Decided by: The t lies between -2 and 2: inconclusive rule.
- Reading: The profile (60-bar fall and 365-bar volatility percentile, unrecorded and needing history before each window) is read from regime == mean_reversion, width is recomputed from prices where 30 past returns exist in the window (else taken as met by the regime), the t sums case deviations per UTC day, and the median split puts locations above the median in the upper half; fewer than 50 cases or days gives not observable.
- Size: unusual move +0.26 % (t 0.87, the cases of one day together: 180 days) per case over 1 bars, 0.050 of the coin's usual move (5.33 %); normal drift in its direction -0.13 %, total +0.13 %; 310 cases
Plan: `steps_cards/03_test_plan/night9_fallcalmwide_run/plans/060-01.b1_falling-calm-high-close-fade_1d.md`
Record: `steps_cards/04_backtest/night9_fallcalmwide_run/backtests/060-01.b1_falling-calm-high-close-fade_1d`
Measure: `measure.py`
