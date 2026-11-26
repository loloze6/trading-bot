---
plan: 041-01_agitated-scaled-rise-next-day-continues_1d
idea: 041-01_agitated-scaled-rise-next-day-continues
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: forecast-weighted mean next-day excess return (over coin mean daily return) on forecast > 0: -0.00193593; t of the weighted mean, cases of one day clustered: -1.11425 (threshold: confirm: positive with t >= 2 and supporting check passes; reject: negative with t <= -2)
- Supporting check: mean next-day excess return, top third minus bottom third by forecast: 0.00152886, passed: True
- Counts: distinct days with forecast > 0: 1517, cases with forecast > 0: 3955
- Decided by: The main measure's t lies between -2 and 2, which the plan calls inconclusive.
- Reading: The agitated profile is read from the recorded regime (not 'chop', i.e. the vol-percentile veto did not fire) since the detector's component is not recorded; the 1-bar horizon uses every bar; the day-clustered t is the ratio-estimator t with per-day summed residuals f*(excess - mean); thirds are the lowest and highest floor(n/3) cases ranked by forecast pooled across coins; the 100-day minimum counts distinct UTC days of forecast > 0 cases with a next-day return.
- Size: unusual move -0.36 % (t -2.12, the cases of one day together: 1121 days) per case over 1 bars, -0.080 of the coin's usual move (4.73 %); normal drift in its direction +0.13 %, total -0.23 %; 2519 cases
Plan: `steps_cards/03_test_plan/night7_chopreversal_run/plans/041-01_agitated-scaled-rise-next-day-continues_1d.md`
Record: `steps_cards/04_backtest/night7_chopreversal_run/backtests/041-01_agitated-scaled-rise-next-day-continues_1d`
Measure: `measure.py`
