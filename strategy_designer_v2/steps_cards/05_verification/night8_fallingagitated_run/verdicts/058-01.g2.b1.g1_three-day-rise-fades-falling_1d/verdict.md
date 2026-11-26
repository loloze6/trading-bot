---
plan: 058-01.g2.b1.g1_three-day-rise-fades-falling_1d
idea: 058-01.g2.b1.g1_three-day-rise-fades-falling
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-direction unusual 3-day move of bets (vs coin's normal drift): 0.00696698; t with same-day cases summed: 1.46226 (threshold: confirm: mean > 0 with t >= 2 and slope > 0; reject: t <= -2; at least 30 distinct case days)
- Supporting check: OLS slope of unusual short move on |forecast|: -0.000314506, passed: False
- Counts: cases: 952, distinct case days: 391
- Decided by: The t lies between -2 and 2.
- Reading: Profile taken from the recorded regime ('unknown' = falling agitated) and rise from the scaled_rise raw value; a case is the first short bet in each non-overlapping 3-bar grid cell of a window, its return taken from that bet bar's close 3 bars ahead inside the window; the day-clustered t uses a G/(G-1) correction so that one case per day gives the ordinary t.
- Size: unusual move +0.70 % (t 1.46, the cases of one day together: 391 days) per case over 3 bars, 0.075 of the coin's usual move (8.85 %); normal drift in its direction -0.44 %, total +0.26 %; 952 cases
Plan: `steps_cards/03_test_plan/night8_fallingagitated_run/plans/058-01.g2.b1.g1_three-day-rise-fades-falling_1d.md`
Record: `steps_cards/04_backtest/night8_fallingagitated_run/backtests/058-01.g2.b1.g1_three-day-rise-fades-falling_1d`
Measure: `measure.py`
