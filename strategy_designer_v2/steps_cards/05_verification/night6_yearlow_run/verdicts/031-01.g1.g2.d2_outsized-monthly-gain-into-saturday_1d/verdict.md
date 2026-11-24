---
plan: 031-01.g1.g2.d2_outsized-monthly-gain-into-saturday_1d
idea: 031-01.g1.g2.d2_outsized-monthly-gain-into-saturday
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of forecast x excess Saturday return over Friday cases: 0.0775323; t of the mean, cases of the same Friday summed: 2.58276 (threshold: confirm: mean > 0 with t >= 2 and supporting check passes; reject: mean < 0 with t <= -2)
- Supporting check: top fifth minus rest of positive cases, excess Saturday return: -0.000972822, passed: False
- Counts: cases: 1155, distinct Fridays: 314
- Decided by: Inconclusive rule: t >= 2 but the supporting check (top fifth minus rest above 0) failed.
- Reading: A case is a Friday-start (UTC) bar with forecast > 0 whose next row in the same window is the Saturday bar; the coin's mean daily return is over all next-row returns of all its windows; the day-clustered t sums deviations per Friday with a D/(D-1) correction; the top fifth per coin is the ceil(20%) highest forecasts (stable order on ties); fewer than the plan's minimum counts gives 'not observable'.
- Size: unusual move +0.66 % (t 2.66, the cases of one day together: 262 days) per case over 1 bars, 0.133 of the coin's usual move (4.73 %); normal drift in its direction +0.13 %, total +0.79 %; 812 cases
Plan: `steps_cards/03_test_plan/night6_yearlow_run/plans/031-01.g1.g2.d2_outsized-monthly-gain-into-saturday_1d.md`
Record: `steps_cards/04_backtest/night6_yearlow_run/backtests/031-01.g1.g2.d2_outsized-monthly-gain-into-saturday_1d`
Measure: `measure.py`
