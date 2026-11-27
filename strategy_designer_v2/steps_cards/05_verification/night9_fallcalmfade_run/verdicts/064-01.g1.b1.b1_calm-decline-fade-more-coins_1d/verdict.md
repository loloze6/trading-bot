---
plan: 064-01.g1.b1.b1_calm-decline-fade-more-coins_1d
idea: 064-01.g1.b1.b1_calm-decline-fade-more-coins
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-direction next-day unusual move (return minus coin drift): -0.000430244; t of the mean, cases of one day taken together: -0.19245 (threshold: confirm: mean > 0 with day-clustered t >= 2; reject: t <= -2)
- Supporting check: top-minus-bottom half (median |forecast|) mean unusual move: 0.000556284, passed: True
- Counts: cases: 655, distinct days: 331
- Decided by: The main measure's t is between -2 and 2.
- Reading: The situation is taken as zr >= 1 (the recorded raw value of the identical 'rise' component, recomputed from closes as return / 20-return std if missing) with the regime 'trending' standing for the falling-calm profile (its detector components are not recorded and the 365-bar percentile cannot be rebuilt inside a window), on the short side; cases are the workflow's short bets (band 2) on every bar of the 1-bar grid; the median split puts |forecast| above the median in the top half and at or below it in the bottom half; the plan's 'fewer than 50 cases or 30 days' is applied as the minimum counts (not observable).
- Size: unusual move -0.04 % (t -0.19, the cases of one day together: 331 days) per case over 1 bars, -0.007 of the coin's usual move (5.33 %); normal drift in its direction -0.13 %, total -0.17 %; 655 cases
Plan: `steps_cards/03_test_plan/night9_fallcalmfade_run/plans/064-01.g1.b1.b1_calm-decline-fade-more-coins_1d.md`
Record: `steps_cards/04_backtest/night9_fallcalmfade_run/backtests/064-01.g1.b1.b1_calm-decline-fade-more-coins_1d`
Measure: `measure.py`
