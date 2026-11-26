---
plan: 039-01_agitated-swing-fall-low-close-rebound_1d
idea: 039-01_agitated-swing-fall-low-close-rebound
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of next-day return minus coin mean, on forecast, forecast > 0, day-summed cases: 0.000521419; t of the OLS slope: 3.86196 (threshold: confirm: slope > 0 with t >= 2 and supporting check passes; reject: slope < 0 with t <= -2)
- Supporting check: book mean daily return before costs minus gain from market's rise: 0.000517164, passed: True
- Counts: days with a positive forecast: 1463, days in the regression: 1449
- Decided by: The slope is positive with t >= 2 and the supporting check passes (confirm rule).
- Reading: Situation = raw FallCloseLocation value > 0 on a bar whose close is below the previous close (first bar of a window judged on the raw value alone) with regime not 'chop', long side; same-day cases are summed into one case by summing their forecasts and their excess next-day returns, then an OLS slope with intercept is fitted across days; the 100-day minimum counts distinct days with any coin's forecast above 0; the book's return before costs is the position held times the coin's next-bar return, averaged over coins each day.
- Size: unusual move +0.37 % (t 1.93, the cases of one day together: 1078 days) per case over 1 bars, 0.083 of the coin's usual move (4.73 %); normal drift in its direction +0.13 %, total +0.50 %; 2520 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.0002398 on the check folds against +0.0005214 on every fold
Plan: `steps_cards/03_test_plan/night7_steadydecline_run/plans/039-01_agitated-swing-fall-low-close-rebound_1d.md`
Record: `steps_cards/04_backtest/night7_steadydecline_run/backtests/039-01_agitated-swing-fall-low-close-rebound_1d`
Measure: `measure.py`
