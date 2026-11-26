---
plan: 058-01.g2.b1.d3_one-day-rise-fades-over-5-days_1d
idea: 058-01.g2.b1.d3_one-day-rise-fades-over-5-days
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 5-bar move of short bets, in the short direction: 0.00742392; t of the mean, cases of one day taken together: 1.15687 (threshold: confirm: mean > 0 with t >= 2 (and supporting check > 0); reject: mean < 0 with t <= -2)
- Supporting check: mean unusual move, larger-|forecast| half minus smaller half: 0.015328, passed: True
- Counts: distinct case days: 410, cases: 1052
- Decided by: The t lies between -2 and 2 (or sign and t disagree): inconclusive.
- Reading: Profile read from the recorded regime ('unknown' = falling agitated, the config's only active regime); a case is the first short bet (forecast magnitude rising >= 2 points from its lowest level since the last bet) in each 5-bar grid cell of a window, measured from that bet's close over 5 bars within the window; the larger half is |forecast| strictly above the median; the day-clustered t uses deviations from the mean summed per UTC day with a D/(D-1) correction; the plan's 'fewer than 30 distinct case days' minimum is reported as 'not observable'.
- Size: unusual move +0.74 % (t 1.16, the cases of one day together: 410 days) per case over 5 bars, 0.060 of the coin's usual move (11.68 %); normal drift in its direction -0.74 %, total +0.00 %; 1052 cases
Plan: `steps_cards/03_test_plan/night8_fallingagitated_run/plans/058-01.g2.b1.d3_one-day-rise-fades-over-5-days_1d.md`
Record: `steps_cards/04_backtest/night8_fallingagitated_run/backtests/058-01.g2.b1.d3_one-day-rise-fades-over-5-days_1d`
Measure: `measure.py`
