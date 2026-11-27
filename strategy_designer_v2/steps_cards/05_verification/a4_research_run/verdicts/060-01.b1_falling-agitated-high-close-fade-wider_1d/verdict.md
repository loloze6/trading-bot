---
plan: 060-01.b1_falling-agitated-high-close-fade-wider_1d
idea: 060-01.b1_falling-agitated-high-close-fade-wider
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: |forecast|-weighted mean unusual move of the short over the next bar: 0.00299489; t of the mean, cases of one day as one piece of evidence: 1.0111 (threshold: positive with day-clustered t >= 2 to confirm; negative with t <= -2 to reject; at least 30 distinct days)
- Supporting check: mean unusual move, larger minus smaller |forecast| half (Welch), Welch t = 1.538: 0.00551419, passed: True
- Counts: short cases: 1051, distinct days with a short case: 534
- Decided by: The main measure's t lies between -2 and 2.
- Reading: The situation is location (close-low)/(high-low) >= 0.5 from prices on bars the detector put in 'mean_reversion' (the profile vetoes are read from the regime column since its components are not recorded) with the raw range position >= 0 where recorded; the day-clustered t of the weighted mean sums the weighted deviations per UTC day; the supporting halves are |forecast| above the median versus at or below it, compared by their unweighted mean unusual moves.
- Size: unusual move +0.36 % (t 1.33, the cases of one day together: 412 days) per case over 1 bars, 0.068 of the coin's usual move (5.16 %); normal drift in its direction -0.09 %, total +0.27 %; 740 cases
Plan: `steps_cards/03_test_plan/a4_research_run/plans/060-01.b1_falling-agitated-high-close-fade-wider_1d.md`
Record: `steps_cards/04_backtest/a4_research_run/backtests/060-01.b1_falling-agitated-high-close-fade-wider_1d`
Measure: `measure.py`
