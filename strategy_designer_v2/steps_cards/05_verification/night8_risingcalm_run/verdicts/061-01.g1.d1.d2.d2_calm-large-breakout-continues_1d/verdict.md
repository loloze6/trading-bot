---
plan: 061-01.g1.d1.d2.d2_calm-large-breakout-continues_1d
idea: 061-01.g1.d1.d2.d2_calm-large-breakout-continues
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of 5-day excess return on case forecast: 0.00132568; day-clustered t: 1.05971 (threshold: confirm: slope > 0 with t >= 2 (and supporting difference > 0); reject: slope < 0 with t <= -2)
- Supporting check: mean 5-day excess: cases minus far-below rises: 0.0147737, passed: True
- Counts: cases: 211, distinct days: 158, far-below rises: 240
- Decided by: The slope's |t| is below 2.
- Reading: Situation = close equal to the highest of the last 20 closes (today included, bars with fewer than 20 closes in the window left out) with a positive raw rise_sd (recomputed from prices where not recorded) outside the 'chop' profile regime, side long; a case is the first bet (forecast rise >= 2 from its low on the long side since the last bet) in each 5-bar grid cell of a window, with its 5-bar return from that bar; the coin's mean 5-day return uses the non-overlapping grid of all its windows; t uses day-clustered sandwich errors with the CR1 small-sample factor; the far-below rises are, inside non-'chop' bars, positive rises with recomputed 30-day-std size within [min, max] of the cases' raw sizes and close <= 95% of the 20-day closing high, read once per grid cell; the plan's 'fewer than 30 cases/days' is reported as not observable.
- Size: unusual move +0.07 % (t 0.09, the cases of one day together: 158 days) per case over 5 bars, -0.015 of the coin's usual move (10.60 %); normal drift in its direction +0.62 %, total +0.69 %; 211 cases
Plan: `steps_cards/03_test_plan/night8_risingcalm_run/plans/061-01.g1.d1.d2.d2_calm-large-breakout-continues_1d.md`
Record: `steps_cards/04_backtest/night8_risingcalm_run/backtests/061-01.g1.d1.d2.d2_calm-large-breakout-continues_1d`
Measure: `measure.py`
