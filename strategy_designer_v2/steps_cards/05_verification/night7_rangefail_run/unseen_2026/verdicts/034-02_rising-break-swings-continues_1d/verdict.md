---
plan: 034-02_rising-break-swings-continues_1d
idea: 034-02_rising-break-swings-continues
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: forecast-weighted mean excess 5-bar return: 0.0365219; t of the weighted mean, cases of one day together: 2.18023 (threshold: confirm: mean > 0 with t >= 2 and Spearman > 0; reject: mean < 0 with t <= -2)
- Supporting check: Spearman correlation of forecast with 5-bar excess return: -0.00525749, passed: False
- Counts: cases: 122, distinct days: 64
- Decided by: t >= 2 but the Spearman correlation is at or below 0, which the plan calls inconclusive.
- Reading: A case is a holding-period bet of the forecast (a rise of at least 2 points from its lowest level on its side since the last bet), the first one in each 5-bar grid cell of a window; the t of the weighted mean sums the weighted deviations per day; the plan's 'fewer than 30 cases/days' is reported as not observable.
- Size: unusual move +3.98 % (t 2.79, the cases of one day together: 64 days) per case over 5 bars, 0.358 of the coin's usual move (9.44 %); normal drift in its direction +0.44 %, total +4.43 %; 122 cases
Plan: `steps_cards/03_test_plan/night7_rangefail_run/plans/034-02_rising-break-swings-continues_1d.md`
Record: `steps_cards/04_backtest/night7_rangefail_run/unseen_2026/backtests/034-02_rising-break-swings-continues_1d`
Measure: `measure.py`
