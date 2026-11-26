---
plan: 074-01_falling-wide-up-day-fade_1d
idea: 074-01_falling-wide-up-day-fade
fit: adapted
status: inconclusive
---
Situation check: 97 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean next-day return minus drift, short direction, over forecast <= -2: 0.00476677; t of the mean, cases of one day taken together: 1.2774 (threshold: confirm: mean is a fall with day-clustered t >= 2 over >= 30 case-days; reject: t <= -2 over >= 30 case-days)
- Supporting check: OLS slope of next-day return minus drift on forecast (positive, t >= 1): -0.254954, passed: False
- Counts: cases: 440, case-days: 258, active bars: 866
- Decided by: The t of the mean unusual move lies between -2 and 2 (any other result).
- Reading: Falling market read as the config's profile (60-bar close change in percent below -10), with the bar's regime used only where a window lacks the bars to compute a condition; positive forecasts count as off side; cases are forecast <= -2 per the plan, drift is the coin's mean 1-bar return over all windows, the day-clustered t sums deviations per UTC day with a D/(D-1) factor, and the slope t is ordinary OLS across cases; fewer than 30 case-days gives 'not observable'.
- Size: unusual move +0.56 % (t 1.43, the cases of one day together: 234 days) per case over 1 bars, 0.125 of the coin's usual move (4.78 %); normal drift in its direction -0.12 %, total +0.43 %; 396 cases
Plan: `steps_cards/03_test_plan/night9_chopdeep_run/plans/074-01_falling-wide-up-day-fade_1d.md`
Record: `steps_cards/04_backtest/night9_chopdeep_run/backtests/074-01_falling-wide-up-day-fade_1d`
Measure: `measure.py`
