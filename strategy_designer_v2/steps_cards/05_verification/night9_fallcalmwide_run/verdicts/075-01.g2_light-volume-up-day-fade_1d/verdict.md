---
plan: 075-01.g2_light-volume-up-day-fade_1d
idea: 075-01.g2_light-volume-up-day-fade
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-direction unusual 1-bar move on bars with forecast <= -2: 0.00235372; t of the mean, cases of one day summed together: 2.40911 (threshold: confirm: mean > 0 with day-clustered t >= 2 and supporting check passes; reject: mean < 0 with t <= -2; at least 300 distinct case days)
- Supporting check: unusual move of top third minus bottom third by abs(forecast): -0.000541366, passed: False
- Counts: distinct case days: 1995, cases: 9881
- Decided by: Confirming t >= 2 but the supporting check (top third minus bottom third above 0) failed.
- Reading: Up day taken as close above the prior close within the window (the detector's regime on a window's first bar), light volume as the recorded centred volume ratio below 0; horizon 1 bar so every bar is a grid point; normal drift is each coin's mean 1-bar return over all its windows; the t sums case deviations per UTC day (no small-sample correction); thirds are equal-size splits of the cases sorted by abs(forecast); fewer than 300 case days gives 'not observable'.
- Size: unusual move +0.26 % (t 2.45, the cases of one day together: 1819 days) per case over 1 bars, 0.046 of the coin's usual move (5.31 %); normal drift in its direction -0.15 %, total +0.11 %; 7776 cases
Plan: `steps_cards/03_test_plan/night9_fallcalmwide_run/plans/075-01.g2_light-volume-up-day-fade_1d.md`
Record: `steps_cards/04_backtest/night9_fallcalmwide_run/backtests/075-01.g2_light-volume-up-day-fade_1d`
Measure: `measure.py`
