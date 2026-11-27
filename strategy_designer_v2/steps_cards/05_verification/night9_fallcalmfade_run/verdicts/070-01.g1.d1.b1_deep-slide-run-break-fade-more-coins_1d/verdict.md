---
plan: 070-01.g1.d1.b1_deep-slide-run-break-fade-more-coins_1d
idea: 070-01.g1.d1.b1_deep-slide-run-break-fade-more-coins
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-direction next-day unusual move (return minus coin drift, negated): 0.00499848; t of the mean, cases clustered by day: 1.60454 (threshold: mean > 0 with t >= 2 to confirm; mean < 0 with t <= -2 to reject)
- Supporting check: OLS slope of unusual move on abs(forecast): 0.00327953, passed: True
- Counts: cases: 405, distinct days: 218
- Decided by: Inconclusive rule: the t lies between -2 and 2.
- Reading: Case bars are every bar with forecast below 0 whose next close is in the same window, the drift is the coin's mean daily return over all its windows, the t clusters the cases by UTC day (deviations summed per day, G/(G-1) correction), the slope is ordinary least squares on abs(forecast), and both 30-case and 30-day minimums are treated as minimum counts for observability.
- Size: unusual move +0.50 % (t 1.61, the cases of one day together: 218 days) per case over 1 bars, 0.111 of the coin's usual move (5.21 %); normal drift in its direction -0.13 %, total +0.37 %; 405 cases
Plan: `steps_cards/03_test_plan/night9_fallcalmfade_run/plans/070-01.g1.d1.b1_deep-slide-run-break-fade-more-coins_1d.md`
Record: `steps_cards/04_backtest/night9_fallcalmfade_run/backtests/070-01.g1.d1.b1_deep-slide-run-break-fade-more-coins_1d`
Measure: `measure.py`
