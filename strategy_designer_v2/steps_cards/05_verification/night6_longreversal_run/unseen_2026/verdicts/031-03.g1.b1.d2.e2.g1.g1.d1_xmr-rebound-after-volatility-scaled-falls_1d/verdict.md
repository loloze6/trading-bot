---
plan: 031-03.g1.b1.d2.e2.g1.g1.d1_xmr-rebound-after-volatility-scaled-falls_1d
idea: 031-03.g1.b1.d2.e2.g1.g1.d1_xmr-rebound-after-volatility-scaled-falls
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: forecast-weighted mean next-day excess return over XMR's mean daily return (bars with forecast > 0): 0.00308597; t of the forecast-weighted mean: 0.637165 (threshold: confirm: > 0 with t >= 2 (and top-third minus bottom-third > 0); reject: < 0 with t <= -2)
- Supporting check: mean next-day excess return, top third by forecast minus bottom third: 0.00214244, passed: True
- Counts: bars with forecast > 0: 163, bars with forecast > 0 (incl. without next-day return): 163
- Decided by: The t of the forecast-weighted mean excess return lies between -2 and 2, meeting neither the confirm nor the reject rule.
- Reading: Bars with forecast > 0 counted are those with a next-day return inside their window; the coin's mean daily return is the mean of all 1-bar returns over all windows; the t of the weighted mean uses the weighted standard error sqrt(n/(n-1) * sum(w^2 (x-m)^2)) / sum(w); thirds are the floor(n/3) lowest and highest forecasts (stable sort); fewer than 100 such bars is reported as not observable.
- Size: unusual move +0.22 % (t 0.56, the cases of one day together: 93 days) per case over 1 bars, 0.052 of the coin's usual move (4.27 %); normal drift in its direction +0.16 %, total +0.39 %; 93 cases
Plan: `steps_cards/03_test_plan/night6_longreversal_run/plans/031-03.g1.b1.d2.e2.g1.g1.d1_xmr-rebound-after-volatility-scaled-falls_1d.md`
Record: `steps_cards/04_backtest/night6_longreversal_run/unseen_2026/backtests/031-03.g1.b1.d2.e2.g1.g1.d1_xmr-rebound-after-volatility-scaled-falls_1d`
Measure: `measure.py`
