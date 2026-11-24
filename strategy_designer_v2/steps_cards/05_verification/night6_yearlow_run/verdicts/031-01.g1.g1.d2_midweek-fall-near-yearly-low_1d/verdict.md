---
plan: 031-01.g1.g1.d2_midweek-fall-near-yearly-low_1d
idea: 031-01.g1.g1.d2_midweek-fall-near-yearly-low
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of forecast/10 x (Saturday return - coin mean daily return) on Friday active bars: 0.00696484; t of the mean, cases grouped by day: 3.87165 (threshold: confirm: day-grouped t >= 2 over >= 100 days with short-side check > 0; reject: t <= -2 over >= 100 days)
- Supporting check: same mean on short-side cases (mean_reversion, forecast < 0) above 0: 0.00455027, passed: True
- Counts: days: 404, short-side cases: 813, cases: 1992
- Decided by: Confirm: the main-measure t is 2 or more over at least 100 days and the short-side check is above 0.
- Reading: The Friday is the bar whose UTC start is a Friday (its close is Friday's close, the next bar Saturday); the midweek return's sign is read from the recorded raw component, else from Thursday/Monday closes, and is skipped when neither exists; the lower half of the 365-day range is read from the recorded regime (mean_reversion), since the detector's Donchian value is not recorded and 365 days of history are not in the windows; Saturday's return is the next row's close over this close inside the window; the day-grouped t sums each day's case deviations from the mean with a G/(G-1) correction; the plan's minimum counts (100 days, 30 short-side cases) are applied first as 'not observable'.
- Size: unusual move +0.53 % (t 3.57, the cases of one day together: 402 days) per case over 1 bars, 0.112 of the coin's usual move (4.73 %); normal drift in its direction +0.02 %, total +0.56 %; 1716 cases
Plan: `steps_cards/03_test_plan/night6_yearlow_run/plans/031-01.g1.g1.d2_midweek-fall-near-yearly-low_1d.md`
Record: `steps_cards/04_backtest/night6_yearlow_run/backtests/031-01.g1.g1.d2_midweek-fall-near-yearly-low_1d`
Measure: `measure.py`
