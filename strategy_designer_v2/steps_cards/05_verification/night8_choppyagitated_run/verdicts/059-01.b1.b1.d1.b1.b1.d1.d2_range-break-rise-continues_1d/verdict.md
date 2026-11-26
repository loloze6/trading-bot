---
plan: 059-01.b1.b1.d1.b1.b1.d1.d2_range-break-rise-continues_1d
idea: 059-01.b1.b1.d1.b1.b1.d1.d2_range-break-rise-continues
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: forecast-weighted mean excess 14-bar return: 0.0448688; t of the weighted mean, cases of one day pooled: 1.2566 (threshold: confirm: mean > 0 with t >= 2 and slope > 0; reject: mean < 0 with t <= -2)
- Supporting check: OLS slope of excess 14-bar return on forecast: 0.00622915, passed: True
- Counts: grid bars with forecast > 0: 180, distinct days: 79
- Decided by: t between -2 and 2: neither the confirm nor the reject rule is met
- Reading: grid at positions 0,14,28,... of each window with the 14-bar return inside the window; drift = coin's mean 14-bar return on that grid over all its windows; t = weighted mean over a standard error from the forecast-weighted deviations summed per UTC day (with G/(G-1) correction); the plan's 'fewer than 30 grid bars or 20 days' is treated as a minimum count, giving 'not observable'; profile read from the regime column 'unknown'.
- Size: unusual move +0.45 % (t 0.40, the cases of one day together: 340 days) per case over 14 bars, 0.013 of the coin's usual move (18.92 %); normal drift in its direction +2.23 %, total +2.68 %; 518 cases
Plan: `steps_cards/03_test_plan/night8_choppyagitated_run/plans/059-01.b1.b1.d1.b1.b1.d1.d2_range-break-rise-continues_1d.md`
Record: `steps_cards/04_backtest/night8_choppyagitated_run/backtests/059-01.b1.b1.d1.b1.b1.d1.d2_range-break-rise-continues_1d`
Measure: `measure.py`
