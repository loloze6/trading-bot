---
plan: 031-01.g1.g1.g2.g1.d2_uptrend-thursday-weekend-momentum_1d
idea: 031-01.g1.g1.g2.g1.d2_uptrend-thursday-weekend-momentum
fit: adapted
status: not observable
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of 2-bar excess return on rise14 post_pipeline_value, uptrend Thursday cases: 0.000775032; slope t, clustered by day: 0.720129 (threshold: slope t >= 2 (with forecast-weighted mean excess > 0) confirms; slope t <= -2 rejects)
- Supporting check: forecast-weighted mean 2-bar excess return > 0: 0.0102367, passed: True
- Counts: uptrend Thursday cases with forecast above 0: 77, distinct Thursdays of those cases: 24, uptrend Thursday cases (all, incl. forecast 0): 127, distinct days (clusters): 32
- Decided by: The plan's minimum is not reached: 77 uptrend Thursday cases with a forecast above 0 (100 needed) over 24 distinct Thursdays (60 needed).
- Reading: Thursday-close bars are the bars whose UTC start is a Thursday (next bar a Friday); the 60-day uptrend is close above the close of the bar 60 days earlier in the same window, and active bars where that bar is not in the window are left out of the agreement; the coin's mean 2-bar return uses the non-overlapping grid 0,2,4,... of every window; cases are pooled over all coins with an OLS slope (with intercept) whose t uses a cluster-by-day robust variance with the usual G/(G-1)(N-1)/(N-K) correction; the plan's minimum counts, read on cases with forecast above 0, give 'not observable' when unmet.
- Size: unusual move +0.95 % (t 0.77, the cases of one day together: 22 days) per case over 2 bars, 0.169 of the coin's usual move (4.63 %); normal drift in its direction +0.10 %, total +1.05 %; 70 cases
Plan: `steps_cards/03_test_plan/night6_yearlow_run/plans/031-01.g1.g1.g2.g1.d2_uptrend-thursday-weekend-momentum_1d.md`
Record: `steps_cards/04_backtest/night6_yearlow_run/unseen_2026/backtests/031-01.g1.g1.g2.g1.d2_uptrend-thursday-weekend-momentum_1d`
Measure: `measure.py`
