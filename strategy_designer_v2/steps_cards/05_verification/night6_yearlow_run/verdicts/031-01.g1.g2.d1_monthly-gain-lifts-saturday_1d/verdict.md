---
plan: 031-01.g1.g2.d1_monthly-gain-lifts-saturday_1d
idea: 031-01.g1.g2.d1_monthly-gain-lifts-saturday
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: forecast-weighted mean Saturday excess return over the coin's mean daily return: 0.00835242; t of the weighted mean, cases of one day summed: 2.88957 (threshold: confirm: weighted mean excess > 0 with t >= 2 and slope > 0; reject: weighted mean excess < 0 with t <= -2; at least 100 cases)
- Supporting check: least-squares slope of Saturday excess on post_pipeline_value > 0: 0.000482159, passed: True
- Counts: cases: 1180, days: 316
- Decided by: The weighted mean excess is positive with t >= 2 and the slope on the forecast is positive (confirm rule).
- Reading: A Friday-close bar is a bar opening on a Friday UTC (its next bar is Saturday); the situation's gain is the recorded gain20 last_history_value (recomputed from closes if missing) > 0; Saturday's return is the next row's close over this close inside the window; the coin's mean daily return is the mean of all 1-bar returns over all its windows; the t of the forecast-weighted mean uses a day-clustered standard error (per day, the sum of forecast x (excess - weighted mean)); the 100-case minimum counts all cases with a positive forecast and a valid Saturday return across all coins.
- Size: unusual move +0.61 % (t 2.83, the cases of one day together: 289 days) per case over 1 bars, 0.120 of the coin's usual move (4.78 %); normal drift in its direction +0.12 %, total +0.73 %; 1025 cases
Plan: `steps_cards/03_test_plan/night6_yearlow_run/plans/031-01.g1.g2.d1_monthly-gain-lifts-saturday_1d.md`
Record: `steps_cards/04_backtest/night6_yearlow_run/backtests/031-01.g1.g2.d1_monthly-gain-lifts-saturday_1d`
Measure: `measure.py`
