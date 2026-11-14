---
plan: N7-01_drift-only-near-high_1d_oos
idea: N7-01_drift-only-near-high
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: forecast-weighted mean 5-bar excess return over coin mean: 0.00309059; t of weighted mean: 0.682945 (threshold: positive with t >= 2 confirms; negative with t <= -2 rejects)
- Supporting check: mean 5-bar excess return, flat bars with recent high but close below SMA20: 0.00144706, passed: False
- Counts: non-overlapping active 5-bar blocks: 902, flat below-SMA20 recent-high blocks: 403
- Decided by: The t-statistic is strictly between -2 and 2.
- Reading: Situation = close > SMA20 of closes and a 20-bar closing high within the last 20 bars (the recorded raw BarsSinceHigh > 0 where present, else recomputed from closes, else the regime label where the window start lacks history), long side; the coin's mean 5-bar return is taken over all its non-overlapping grid bars in all windows; the t of the forecast-weighted mean uses the weighted standard error sqrt(n/(n-1)*sum(w^2(x-m)^2))/sum(w); the supporting check's 'excess over holding' is the same excess over the coin's mean 5-bar return, on flat grid bars, and it is reported but does not change the confirm/reject rule.
Plan: `steps_cards/03_test_plan/overnight_run/plans_oos/N7-01_drift-only-near-high_1d_oos.md`
Record: `steps_cards/04_backtest/overnight_run/backtests_oos/N7-01_drift-only-near-high_1d_oos`
Measure: `measure.py`
