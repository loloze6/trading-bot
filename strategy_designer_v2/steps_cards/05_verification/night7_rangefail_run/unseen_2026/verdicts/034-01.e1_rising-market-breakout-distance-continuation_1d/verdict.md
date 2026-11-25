---
plan: 034-01.e1_rising-market-breakout-distance-continuation_1d
idea: 034-01.e1_rising-market-breakout-distance-continuation
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: forecast-weighted mean 3-bar excess return: 0.0280295; t of weighted mean, same-day cases pooled: 1.32891 (threshold: confirm: above 0 with t >= 2 (and slope > 0); reject: below 0 with t <= -2)
- Supporting check: OLS slope of 3-bar excess return on forecast: 0.000492001, passed: True
- Counts: cases: 104, cases on distinct days: 41
- Decided by: The t lies between -2 and 2, which the plan calls inconclusive.
- Reading: Situation = raw distance above prior 20-day closing high > 0 (recomputed from closes where not recorded) and, where 60 bars of the window exist, a positive 60-bar price change as the rising profile, side long; the plan's 'fewer than 30 cases on distinct days' is applied as a minimum count (not observable), the weighted-mean t pools each day's weighted deviations, and the slope is an ordinary least-squares slope of excess return on forecast over all cases.
- Size: unusual move +2.69 % (t 2.50, the cases of one day together: 72 days) per case over 3 bars, 0.332 of the coin's usual move (6.81 %); normal drift in its direction +0.19 %, total +2.88 %; 154 cases
Plan: `steps_cards/03_test_plan/night7_rangefail_run/plans/034-01.e1_rising-market-breakout-distance-continuation_1d.md`
Record: `steps_cards/04_backtest/night7_rangefail_run/unseen_2026/backtests/034-01.e1_rising-market-breakout-distance-continuation_1d`
Measure: `measure.py`
