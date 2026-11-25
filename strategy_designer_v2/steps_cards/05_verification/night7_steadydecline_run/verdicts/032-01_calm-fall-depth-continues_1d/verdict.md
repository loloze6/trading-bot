---
plan: 032-01_calm-fall-depth-continues_1d
idea: 032-01_calm-fall-depth-continues
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: graded short gain vs drift, (-forecast/10) x -(next-day excess return), per-day sums: 0.00590473; t of the mean (per-day sums): 1.42539 (threshold: confirm: mean > 0 with t >= 2 and check passes; reject: mean < 0 with t <= -2)
- Supporting check: deepest-third minus shallowest-third next-day excess return (< 0): -0.00474318, passed: True
- Counts: distinct days with a non-zero forecast: 1028, cases (coin-days): 2484
- Decided by: The main measure's t lies between -2 and 2, which the plan calls inconclusive.
- Reading: The falling calm profile is read from the recorded regime 'unknown' (its detector components are not recorded and the 365-bar volatility percentile cannot be rebuilt inside ~120-bar windows), with the recorded 30-bar change below 0 and a negative forecast; the coin's drift is its mean next-bar return over all its windows; the reported mean and t are over per-day sums of the cases; terciles split the cases ranked by forecast (stable order) into three equal-count groups; the 100-day minimum counts distinct days with a non-zero forecast and a next-day return in the same window.
- Size: unusual move +0.13 % (t 0.51, the cases of one day together: 434 days) per case over 1 bars, 0.030 of the coin's usual move (4.73 %); normal drift in its direction -0.13 %, total -0.00 %; 689 cases
Plan: `steps_cards/03_test_plan/night7_steadydecline_run/plans/032-01_calm-fall-depth-continues_1d.md`
Record: `steps_cards/04_backtest/night7_steadydecline_run/backtests/032-01_calm-fall-depth-continues_1d`
Measure: `measure.py`
