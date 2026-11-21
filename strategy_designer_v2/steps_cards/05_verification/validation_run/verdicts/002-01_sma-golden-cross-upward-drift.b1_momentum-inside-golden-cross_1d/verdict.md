---
plan: 002-01_sma-golden-cross-upward-drift.b1_momentum-inside-golden-cross_1d
idea: 002-01_sma-golden-cross-upward-drift.b1_momentum-inside-golden-cross
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of next-20-bar excess return on forecast, trending grid bars: 0.00168476; t of OLS slope: 1.13298 (threshold: t >= 2 confirms (with positive timing), t <= -2 rejects, on at least 50 grid cases)
- Supporting check: trending-regime book mean daily return minus market-rise gain (timing), before costs: 0.000653584, passed: True
- Counts: trending-regime grid cases: 414
- Decided by: Slope t lies between -2 and 2.
- Reading: Trending bars are those with regime=='trending'; the coin's mean 20-bar return is the mean over all its non-overlapping grid returns in all windows; the regression is pooled OLS with an intercept; the timing part uses held position x (next daily return minus the coin's all-window mean daily return) on trending-regime bars, averaged across coins per (window, day) and then over days.
- Size: unusual move +0.78 % per case over 20 bars, 0.007 of the coin's usual move (21.24 %); normal drift in its direction -0.08 %, total +0.70 %; 422 cases
Plan: `steps_cards/03_test_plan/plans/002-01_sma-golden-cross-upward-drift.b1_momentum-inside-golden-cross_1d.md`
Record: `steps_cards/04_backtest/backtests/002-01_sma-golden-cross-upward-drift.b1_momentum-inside-golden-cross_1d`
Measure: `measure.py`
