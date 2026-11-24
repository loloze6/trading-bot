---
plan: 031-01.g1.g1.g2.g1.d2_uptrend-thursday-weekend-momentum_1d
idea: 031-01.g1.g1.g2.g1.d2_uptrend-thursday-weekend-momentum
fit: adapted
status: inconclusive
---
Situation check: 99 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of 2-bar excess return on rise14 post_pipeline_value, uptrend Thursday cases: -0.000198094; slope t, clustered by day: -0.200973 (threshold: slope t >= 2 (with forecast-weighted mean excess > 0) confirms; slope t <= -2 rejects)
- Supporting check: forecast-weighted mean 2-bar excess return > 0: -0.00555727, passed: False
- Counts: uptrend Thursday cases with forecast above 0: 225, distinct Thursdays of those cases: 94, uptrend Thursday cases (all, incl. forecast 0): 318, distinct days (clusters): 100
- Decided by: Inconclusive rule met: the slope's t is between -2 and 2.
- Reading: Thursday-close bars are the bars whose UTC start is a Thursday (next bar a Friday); the 60-day uptrend is close above the close of the bar 60 days earlier in the same window, and active bars where that bar is not in the window are left out of the agreement; the coin's mean 2-bar return uses the non-overlapping grid 0,2,4,... of every window; cases are pooled over all coins with an OLS slope (with intercept) whose t uses a cluster-by-day robust variance with the usual G/(G-1)(N-1)/(N-K) correction; the plan's minimum counts, read on cases with forecast above 0, give 'not observable' when unmet.
- Size: unusual move -0.40 % (t -0.46, the cases of one day together: 87 days) per case over 2 bars, -0.027 of the coin's usual move (11.41 %); normal drift in its direction +1.92 %, total +1.52 %; 202 cases
Plan: `steps_cards/03_test_plan/night6_yearlow_run/plans/031-01.g1.g1.g2.g1.d2_uptrend-thursday-weekend-momentum_1d.md`
Record: `steps_cards/04_backtest/night6_yearlow_run/unseen_2016_2017/backtests/031-01.g1.g1.g2.g1.d2_uptrend-thursday-weekend-momentum_1d`
Measure: `measure.py`
