---
plan: 059-01.b1.b1.d2_choppy-calm-rise-up-month_1d
idea: 059-01.b1.b1.d2_choppy-calm-rise-up-month
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 14-bar move of the cases (forecast rise >= 2, one per 14-bar grid cell): 0.00973816; t of the mean, cases of one day together: 0.862262 (threshold: confirm: mean > 0 with day-clustered t >= 2 and slope > 0; reject: t <= -2 or slope t <= -2)
- Supporting check: slope of drift-adjusted 14-bar return on forecast (grid cells, forecast > 0): 0.00817537, passed: True
- Counts: cases: 431, distinct days: 297, slope grid cells: 129, active bars: 1908
- Decided by: Neither the confirm nor the reject rule is met (t between -2 and 2, or slope not above 0 without significance).
- Reading: Situation = regime 'trending' (choppy-calm profile plus 30-day return > 0, recomputed from prices where 30 prior bars exist) with week_rise raw value > 0, side long; a case is the first long-side bet (forecast rise >= 2 from its lowest level since the last bet, reset at flat) in each 14-bar grid cell of its window, its 14-bar return read inside the window; the drift is the coin's mean 14-bar return on the grid over all its windows; the t clusters cases by UTC signal day with a G/(G-1) correction; the slope is OLS on grid bars with forecast > 0; the plan's 'fewer than 30 cases/days' is reported as not observable as the workflow requires.
- Size: unusual move +0.97 % (t 0.86, the cases of one day together: 297 days) per case over 14 bars, 0.045 of the coin's usual move (18.92 %); normal drift in its direction +2.19 %, total +3.16 %; 431 cases
Plan: `steps_cards/03_test_plan/night8_choppyagitated_run/plans/059-01.b1.b1.d2_choppy-calm-rise-up-month_1d.md`
Record: `steps_cards/04_backtest/night8_choppyagitated_run/backtests/059-01.b1.b1.d2_choppy-calm-rise-up-month_1d`
Measure: `measure.py`
