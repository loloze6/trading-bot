---
plan: 025-01_downtrend-bounce-given-back.b1_downtrend-bounce-more-coins.b1_outsized-downtrend-bounces-given-back_1d
idea: 025-01_downtrend-bounce-given-back.b1_downtrend-bounce-more-coins.b1_outsized-downtrend-bounces-given-back
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 5-bar move of short cases, in the short direction: 0.00615611; t of the mean: 2.81011 (threshold: positive with t >= 2 (and supporting check) confirms; negative with t <= -2 rejects; else inconclusive)
- Supporting check: mean unusual move at forecast <= -10 minus that at forecast between -2 and -10: -0.00631788, passed: False
- Counts: cases: 2312, cases at forecast -10 or below: 1078, cases with forecast between -2 and -10: 1234
- Decided by: A confirming t with a failed supporting check is inconclusive.
- Reading: A case is the first short bet (|forecast| rising >= 2 from its lowest short level since the last bet, reset at flat) in each 5-bar grid cell of a window, judged on close[t+5]/close[t]-1 minus the coin's mean non-overlapping 5-bar return over all windows; 'between -2 and -10' is read as -10 < forecast <= -2.
- Size: unusual move +0.62 % per case over 5 bars, 0.047 of the coin's usual move (12.45 %); normal drift in its direction -0.76 %, total -0.14 %; 2312 cases
Plan: `steps_cards/03_test_plan/night4_fallingbounce_run/plans/025-01_downtrend-bounce-given-back.b1_downtrend-bounce-more-coins.b1_outsized-downtrend-bounces-given-back_1d.md`
Record: `steps_cards/04_backtest/night4_fallingbounce_run/backtests/025-01_downtrend-bounce-given-back.b1_downtrend-bounce-more-coins.b1_outsized-downtrend-bounces-given-back_1d`
Measure: `measure.py`
