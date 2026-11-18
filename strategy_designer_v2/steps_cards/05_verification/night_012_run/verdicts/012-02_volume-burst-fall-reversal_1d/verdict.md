---
plan: 012-02_volume-burst-fall-reversal_1d
idea: 012-02_volume-burst-fall-reversal
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of 3-bar excess return on forecast: 0.000595545; OLS slope t: 2.48178 (threshold: slope t >= 2 confirms (with positive volume-ratio coefficient); t <= -2 rejects; otherwise inconclusive)
- Supporting check: volume-ratio coefficient in excess ~ volume ratio + fall size: 0.0149757, passed: True
- Counts: independent cases with forecast > 0 on the grid: 2683, cases in the supporting regression: 1999
- Decided by: The slope t is 2 or more and the volume-ratio coefficient in the supporting regression is positive.
- Reading: The coin's mean 3-bar return is the mean of its non-overlapping grid 3-bar returns over all windows; the volume ratio is the bar's volume over the mean of the last 30 volumes including it, and the fall size is minus the bar's return over the 20-bar standard deviation of daily returns including it, both computed within each window (bars without full history left out of the supporting regression, which has an intercept); fewer than 100 cases is reported as not observable.
Plan: `steps_cards/03_test_plan/night_012_run/plans/012-02_volume-burst-fall-reversal_1d.md`
Record: `steps_cards/04_backtest/night_012_run/backtests/012-02_volume-burst-fall-reversal_1d`
Measure: `measure.py`
