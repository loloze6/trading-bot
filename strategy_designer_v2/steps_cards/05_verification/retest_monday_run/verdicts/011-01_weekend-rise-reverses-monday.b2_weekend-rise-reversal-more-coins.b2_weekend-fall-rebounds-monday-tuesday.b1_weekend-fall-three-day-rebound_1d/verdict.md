---
plan: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound_1d
idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of (forecast/10) x excess 3-bar return over Sunday cases: 0.0117239; t of the mean: 4.68065 (threshold: t >= 2 confirms (with supporting check), t <= -2 rejects, with at least 100 cases)
- Supporting check: mean excess 3-bar return, larger-fall half minus smaller-fall half (median forecast split): 0.0175096, passed: True
- Counts: cases: 2215, larger-fall half: 1107, smaller-fall half: 1108
- Decided by: Confirm rule: t of 2 or more with at least 100 cases, and the larger-fall half's mean excess return exceeds the smaller-fall half's.
- Reading: Sunday bars are those whose UTC start is a Sunday; cases need forecast >= 2 and close[t+3] in the same window; the coin's mean 3-bar return uses the non-overlapping grid 0,3,6,... of each window pooled across windows; the larger-fall half is forecast strictly above the median and the smaller-fall half the rest.
- Size: unusual move +0.84 % per case over 3 bars, 0.099 of the coin's usual move (9.14 %); normal drift in its direction +0.49 %, total +1.33 %; 2216 cases
Plan: `steps_cards/03_test_plan/retest_monday_run/plans/011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound_1d.md`
Record: `steps_cards/04_backtest/retest_monday_run/backtests/011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound_1d`
Measure: `measure.py`
