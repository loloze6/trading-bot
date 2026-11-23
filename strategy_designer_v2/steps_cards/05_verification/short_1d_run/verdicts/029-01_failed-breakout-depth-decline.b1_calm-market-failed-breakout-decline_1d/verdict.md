---
plan: 029-01_failed-breakout-depth-decline.b1_calm-market-failed-breakout-decline_1d
idea: 029-01_failed-breakout-depth-decline.b1_calm-market-failed-breakout-decline
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 5-bar move in the short direction over short-bet cases: -0.00113649; t of the mean: -0.266362 (threshold: confirm if mean > 0 with t >= 2 (and supporting check passes); reject if mean < 0 with t <= -2)
- Supporting check: mean unusual move of top half minus bottom half by |forecast|: None, passed: False
- Counts: independent cases: 615, top half cases: 0, bottom half cases: 615
- Decided by: The t lies between -2 and 2.
- Reading: A case is the first short bet (forecast falling at least 2 points below its highest short-side level since the last bet, reset to 0 on flat or long bars) inside each 5-bar grid cell counted from each window's first row, cases whose 5-bar return would leave the window are dropped, and the median split puts |forecast| strictly above the median in the top half.
- Size: unusual move -0.11 % per case over 5 bars, -0.007 of the coin's usual move (10.60 %); normal drift in its direction -0.58 %, total -0.69 %; 615 cases
Plan: `steps_cards/03_test_plan/short_1d_run/plans/029-01_failed-breakout-depth-decline.b1_calm-market-failed-breakout-decline_1d.md`
Record: `steps_cards/04_backtest/short_1d_run/backtests/029-01_failed-breakout-depth-decline.b1_calm-market-failed-breakout-decline_1d`
Measure: `measure.py`
