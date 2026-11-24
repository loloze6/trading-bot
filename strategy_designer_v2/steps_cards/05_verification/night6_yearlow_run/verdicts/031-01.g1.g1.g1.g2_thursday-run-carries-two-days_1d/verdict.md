---
plan: 031-01.g1.g1.g1.g2_thursday-run-carries-two-days_1d
idea: 031-01.g1.g1.g1.g2_thursday-run-carries-two-days
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of forecast/10 x drift-removed 2-bar return on Thursday-close bars: 0.00774074; t of the mean, cases of one day summed: 2.90466 (threshold: t >= 2 confirms (with the check passing), t <= -2 rejects, otherwise inconclusive)
- Supporting check: top third minus bottom third of forecasts, mean drift-removed 2-bar return, above 0: 0.0119481, passed: True
- Counts: Thursday cases with a nonzero forecast: 2465, distinct days: 411
- Decided by: The main measure's t is >= 2 and the top-minus-bottom-third check is above 0 (confirm rule).
- Reading: Thursday-close bars are bars starting Thursday UTC with a nonzero forecast and a full 2-bar return inside the window (weekly spacing makes them non-overlapping), the drift is each coin's mean 2-bar return on the non-overlapping grid 0,2,4,... of all its windows, and the thirds are the floor(n/3) lowest and highest pooled forecasts.
- Size: unusual move +0.50 % (t 2.20, the cases of one day together: 411 days) per case over 2 bars, 0.072 of the coin's usual move (6.58 %); normal drift in its direction -0.00 %, total +0.50 %; 2147 cases
Plan: `steps_cards/03_test_plan/night6_yearlow_run/plans/031-01.g1.g1.g1.g2_thursday-run-carries-two-days_1d.md`
Record: `steps_cards/04_backtest/night6_yearlow_run/backtests/031-01.g1.g1.g1.g2_thursday-run-carries-two-days_1d`
Measure: `measure.py`
