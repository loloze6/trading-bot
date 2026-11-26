---
plan: 031-01.b1.e2_wide-day-in-strong-run_1d
idea: 031-01.b1.e2_wide-day-in-strong-run
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: 3-day forward return minus the coin's normal 3-day drift, top-fifth forecast in-rise grid bars: 0.0362285; t of the mean, same-day cases taken together: 1.84184 (threshold: confirm: mean > 0 with day-clustered t >= 2 (and top-minus-bottom > 0); reject: mean < 0 with t <= -2)
- Supporting check: mean excess top fifth minus bottom fifth in-rise (Welch t 2.800): 0.056488, passed: True
- Counts: top-fifth cases on separate days: 73, top-fifth cases: 115, bottom-fifth in-rise cases: 115, in-rise grid bars: 573
- Decided by: The main-measure t lies between -2 and 2 (or the mean's sign disagrees with it), meeting neither rule.
- Reading: The top and bottom fifths are the in-rise (5-day return > 0) bars of the 3-bar grid, pooled over all coins and windows, with forecast at or above the 80th (at or below the 20th) percentile of those bars' forecasts; the day-clustered t sums each day's deviations with a G/(G-1) correction, and the minimum count missed makes the status not observable.
- Size: unusual move +2.74 % (t 2.22, the cases of one day together: 252 days) per case over 3 bars, 0.179 of the coin's usual move (13.83 %); normal drift in its direction +2.73 %, total +5.47 %; 371 cases
Plan: `steps_cards/03_test_plan/night6_indecision_run/plans/031-01.b1.e2_wide-day-in-strong-run_1d.md`
Record: `steps_cards/04_backtest/night6_indecision_run/unseen_2016_2017/backtests/031-01.b1.e2_wide-day-in-strong-run_1d`
Measure: `measure.py`
