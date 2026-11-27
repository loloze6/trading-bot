---
plan: 031-01.g1.g1.g2.g1.d2_uptrend-thursday-weekend-momentum_1d
idea: 031-01.g1.g1.g2.g1.d2_uptrend-thursday-weekend-momentum
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of 2-bar excess return on rise14 post_pipeline_value, uptrend Thursday cases: 0.00121734; slope t, clustered by day: 2.87157 (threshold: slope t >= 2 (with forecast-weighted mean excess > 0) confirms; slope t <= -2 rejects)
- Supporting check: forecast-weighted mean 2-bar excess return > 0: 0.0190745, passed: True
- Counts: uptrend Thursday cases with forecast above 0: 2326, distinct Thursdays of those cases: 430, uptrend Thursday cases (all, incl. forecast 0): 3706, distinct days (clusters): 490
- Decided by: Confirm rule met: the slope's t is 2 or more and the forecast-weighted mean excess return is above 0.
- Reading: Thursday-close bars are the bars whose UTC start is a Thursday (next bar a Friday); the 60-day uptrend is close above the close of the bar 60 days earlier in the same window, and active bars where that bar is not in the window are left out of the agreement; the coin's mean 2-bar return uses the non-overlapping grid 0,2,4,... of every window; cases are pooled over all coins with an OLS slope (with intercept) whose t uses a cluster-by-day robust variance with the usual G/(G-1)(N-1)/(N-K) correction; the plan's minimum counts, read on cases with forecast above 0, give 'not observable' when unmet.
- Size: unusual move +1.54 % (t 3.40, the cases of one day together: 412 days) per case over 2 bars, 0.203 of the coin's usual move (7.64 %); normal drift in its direction +0.32 %, total +1.86 %; 2058 cases
- Direction check on folds A, D (the years step 7 does not explore): not judged: no check fold (the plan has none, or the backtest did not run on its folds)
Plan: `steps_cards/03_test_plan/night6_yearlow_run/plans/031-01.g1.g1.g2.g1.d2_uptrend-thursday-weekend-momentum_1d.md`
Record: `steps_cards/04_backtest/night6_yearlow_run/common/backtests/031-01.g1.g1.g2.g1.d2_uptrend-thursday-weekend-momentum_1d`
Measure: `measure.py`
