---
plan: 059-01.b1.b1.d1.b1.b1.d2_choppy-calm-rise-four-weeks_1d
idea: 059-01.b1.b1.d1.b1.b1.d2_choppy-calm-rise-four-weeks
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: forecast-weighted mean 28-bar excess return (over the coin's normal 28-bar drift): 0.0256593; t of the weighted mean, cases of one day taken together: 0.43113 (threshold: t >= 2 with a positive mean to confirm; t <= -2 to reject)
- Supporting check: upper-half minus lower-half mean excess return at the median forecast (Welch t = 0.363): 0.0227075, passed: True
- Counts: cases with a positive forecast: 97, distinct days: 36, upper half cases: 48, lower half cases: 49
- Decided by: Neither rule met: the main t is between -2 and 2 (or undefined) and no reject condition holds.
- Reading: The 28-bar grid starts at each window's first row with the forward return inside the window; the drift is the coin's mean grid 28-bar return over all its windows; the day-clustered t of the weighted mean is m / (sqrt(G/(G-1) * sum over days of (sum of w*(e-m))^2) / sum w); the upper half is forecast above the median, the lower half at or below it, compared by unweighted means; the plan's minimum of 30 cases on 30 days, when not reached, gives 'not observable'.
- Size: unusual move +0.93 % (t 0.42, the cases of one day together: 267 days) per case over 28 bars, 0.009 of the coin's usual move (28.73 %); normal drift in its direction +4.67 %, total +5.61 %; 403 cases
Plan: `steps_cards/03_test_plan/night8_choppyagitated_run/plans/059-01.b1.b1.d1.b1.b1.d2_choppy-calm-rise-four-weeks_1d.md`
Record: `steps_cards/04_backtest/night8_choppyagitated_run/backtests/059-01.b1.b1.d1.b1.b1.d2_choppy-calm-rise-four-weeks_1d`
Measure: `measure.py`
