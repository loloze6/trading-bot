---
plan: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.d2_volatility-graded-weekend-reversal_1d
idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.d2_volatility-graded-weekend-reversal
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean signed excess 2-day return (Sunday close to Tuesday close) over Sunday cases, before costs: 0.00659743; t of the mean: 6.17951 (threshold: confirm: mean > 0 with t >= 2 (and slope t >= 2); reject: mean < 0 with t <= -2)
- Supporting check: slope of signed excess 2-day return on s20/s60 (recomputed from closes): 0.018569, passed: True
- Counts: Sunday cases: 5169, cases in slope regression: 2601
- Decided by: Main mean positive with t >= 2 and the s20/s60 slope positive with t >= 2.
- Reading: Cases are Sunday (UTC start) bars with nonzero forecast and a close two bars later in the same window, the coin's mean 2-day return is pooled over a 0,2,4,... grid of all its windows, s20/s60 uses within-window daily returns (std ddof 1, cases without 60 returns left out of the regression), and the plan's 300-case minimum is applied as 'not observable'.
- Size: unusual move +0.72 % per case over 2 bars, 0.100 of the coin's usual move (7.48 %); normal drift in its direction +0.01 %, total +0.74 %; 4129 cases
Plan: `steps_cards/03_test_plan/retest_monday_run/plans/011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.d2_volatility-graded-weekend-reversal_1d.md`
Record: `steps_cards/04_backtest/retest_monday_run/backtests/011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.d2_volatility-graded-weekend-reversal_1d`
Measure: `measure.py`
