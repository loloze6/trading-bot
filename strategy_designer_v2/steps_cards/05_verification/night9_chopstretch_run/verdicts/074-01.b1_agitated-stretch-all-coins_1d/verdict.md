---
plan: 074-01.b1_agitated-stretch-all-coins_1d
idea: 074-01.b1_agitated-stretch-all-coins
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: forecast-weighted mean excess 10-bar return: 0.00921072; t of the weighted mean, cases summed per day: 0.679219 (threshold: confirm: > 0 with t >= 2 and deep-minus-shallow > 0; reject: < 0 with t <= -2)
- Supporting check: deep minus shallow mean excess 10-bar return: 0.00203436, passed: True
- Counts: cases: 764, distinct days: 166
- Decided by: The t lies between -2 and 2, which the plan calls inconclusive.
- Reading: Agitated profile read as regime not 'chop' and below the average as raw stretch < 0; cases are grid bars (positions 0,10,20,... per window) with forecast > 0 and a 10-bar return inside the window; the t is the weighted mean over a day-clustered standard error (each day's weighted deviations summed); deep half = forecast strictly above the cases' median, shallow = the rest, compared on unweighted mean excess; the plan's minimum counts not reached give 'not observable'.
- Size: unusual move -0.56 % (t -0.75, the cases of one day together: 467 days) per case over 10 bars, -0.023 of the coin's usual move (15.92 %); normal drift in its direction +1.34 %, total +0.78 %; 1053 cases
Plan: `steps_cards/03_test_plan/night9_chopstretch_run/plans/074-01.b1_agitated-stretch-all-coins_1d.md`
Record: `steps_cards/04_backtest/night9_chopstretch_run/backtests/074-01.b1_agitated-stretch-all-coins_1d`
Measure: `measure.py`
