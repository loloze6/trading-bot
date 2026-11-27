---
plan: 031-03.g1.b1.d2.e2.g1.g1.d1_xmr-rebound-after-volatility-scaled-falls_1d
idea: 031-03.g1.b1.d2.e2.g1.g1.d1_xmr-rebound-after-volatility-scaled-falls
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: forecast-weighted mean next-day excess return over XMR's mean daily return (bars with forecast > 0): 0.00248115; t of the forecast-weighted mean: 4.18455 (threshold: confirm: > 0 with t >= 2 (and top-third minus bottom-third > 0); reject: < 0 with t <= -2)
- Supporting check: mean next-day excess return, top third by forecast minus bottom third: 0.00470773, passed: True
- Counts: bars with forecast > 0: 24840, bars with forecast > 0 (incl. without next-day return): 25109
- Decided by: The forecast-weighted mean excess return is > 0 with t >= 2 and the top-third minus bottom-third difference is > 0.
- Reading: Bars with forecast > 0 counted are those with a next-day return inside their window; the coin's mean daily return is the mean of all 1-bar returns over all windows; the t of the weighted mean uses the weighted standard error sqrt(n/(n-1) * sum(w^2 (x-m)^2)) / sum(w); thirds are the floor(n/3) lowest and highest forecasts (stable sort); fewer than 100 such bars is reported as not observable.
- Size: unusual move +0.06 % (t 0.48, the cases of one day together: 2547 days) per case over 1 bars, 0.010 of the coin's usual move (5.21 %); normal drift in its direction +0.12 %, total +0.18 %; 15850 cases
- Direction check on folds A, D (the years step 7 does not explore): not judged: no check fold (the plan has none, or the backtest did not run on its folds)
Plan: `steps_cards/03_test_plan/night6_longreversal_run/plans/031-03.g1.b1.d2.e2.g1.g1.d1_xmr-rebound-after-volatility-scaled-falls_1d.md`
Record: `steps_cards/04_backtest/night6_longreversal_run/common/backtests/031-03.g1.b1.d2.e2.g1.g1.d1_xmr-rebound-after-volatility-scaled-falls_1d`
Measure: `measure.py`
