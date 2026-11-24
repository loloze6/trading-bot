---
plan: 031-02_extreme-fall-partly-rebounds_1d
idea: 031-02_extreme-fall-partly-rebounds
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess 30-day return of in-regime grid cells: 0.000222316; t clustered by day: 0.00555516 (threshold: mean > 0 with t >= 2 over at least 30 cases (confirm); mean < 0 with t <= -2 over at least 30 cases (reject))
- Supporting check: mean excess return above minus below median forecast: None, passed: False
- Counts: in-regime cases: 52, days: 29, active bars: 1680
- Decided by: The day-clustered t lies between -2 and 2, meeting neither the confirm nor the reject rule.
- Reading: Grid cells are the rows at positions 0, 30, 60, 90 of each window with a forward 30-bar close inside the window; the coin's mean 30-day return is taken over all its grid cells in all windows; the day-clustered t sums the deviations per UTC day with a G/(G-1) correction; the median split compares cases strictly above with cases strictly below the median forecast, ties left out.
- Size: unusual move +8.21 % (t 1.49, the cases of one day together: 66 days) per case over 30 bars, 0.204 of the coin's usual move (25.51 %); normal drift in its direction +5.09 %, total +13.29 %; 81 cases
Plan: `steps_cards/03_test_plan/night6_longreversal_run/plans/031-02_extreme-fall-partly-rebounds_1d.md`
Record: `steps_cards/04_backtest/night6_longreversal_run/backtests/031-02_extreme-fall-partly-rebounds_1d`
Measure: `measure.py`
