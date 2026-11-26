---
plan: 059-01.b1_calm-swing-scaled-move-continues_1d
idea: 059-01.b1_calm-swing-scaled-move-continues
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of 5-bar forward return minus normal drift on forecast (non-overlapping grid): 0.0004374; t of slope, clustered by day: 1.40816 (threshold: confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; else inconclusive)
- Supporting check: none
- Counts: grid cases: 1829, distinct days: 483
- Decided by: Inconclusive rule met: the slope's t lies between -2 and 2.
- Reading: Calm bars are the bars whose recorded regime is the strategy's regime 'unknown' (not the 'chop' veto), the expected side is the sign of the raw scaled move; the regression is pooled OLS with an intercept, the slope's t from standard errors clustered by UTC calendar day (with the usual small-sample factor), and the normal 5-bar drift is the coin's mean 5-bar return over the non-overlapping grids of all its windows.
- Size: unusual move +0.27 % (t 0.91, the cases of one day together: 916 days) per case over 5 bars, 0.027 of the coin's usual move (10.60 %); normal drift in its direction -0.02 %, total +0.25 %; 1595 cases
Plan: `steps_cards/03_test_plan/night8_risingagitated_run/plans/059-01.b1_calm-swing-scaled-move-continues_1d.md`
Record: `steps_cards/04_backtest/night8_risingagitated_run/backtests/059-01.b1_calm-swing-scaled-move-continues_1d`
Measure: `measure.py`
