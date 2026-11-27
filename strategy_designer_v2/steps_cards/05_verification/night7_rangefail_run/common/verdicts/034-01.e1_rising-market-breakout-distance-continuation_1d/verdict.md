---
plan: 034-01.e1_rising-market-breakout-distance-continuation_1d
idea: 034-01.e1_rising-market-breakout-distance-continuation
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: forecast-weighted mean 3-bar excess return: 0.0365401; t of weighted mean, same-day cases pooled: 3.3591 (threshold: confirm: above 0 with t >= 2 (and slope > 0); reject: below 0 with t <= -2)
- Supporting check: OLS slope of 3-bar excess return on forecast: 0.00322241, passed: True
- Counts: cases: 1166, cases on distinct days: 444
- Decided by: The forecast-weighted mean excess return is above 0 with t >= 2 and the slope on the forecast is positive.
- Reading: Situation = raw distance above prior 20-day closing high > 0 (recomputed from closes where not recorded) and, where 60 bars of the window exist, a positive 60-bar price change as the rising profile, side long; the plan's 'fewer than 30 cases on distinct days' is applied as a minimum count (not observable), the weighted-mean t pools each day's weighted deviations, and the slope is an ordinary least-squares slope of excess return on forecast over all cases.
- Size: unusual move +2.45 % (t 5.35, the cases of one day together: 845 days) per case over 3 bars, 0.247 of the coin's usual move (9.27 %); normal drift in its direction +0.50 %, total +2.95 %; 1644 cases
- Direction check on folds A, D (the years step 7 does not explore): not judged: no check fold (the plan has none, or the backtest did not run on its folds)
Plan: `steps_cards/03_test_plan/night7_rangefail_run/plans/034-01.e1_rising-market-breakout-distance-continuation_1d.md`
Record: `steps_cards/04_backtest/night7_rangefail_run/common/backtests/034-01.e1_rising-market-breakout-distance-continuation_1d`
Measure: `measure.py`
