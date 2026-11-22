---
plan: 024-04_downrun-volume-fade-depth-rebound.b2_dips-in-downtrends-keep-falling_4h
idea: 024-04_downrun-volume-fade-depth-rebound.b2_dips-in-downtrends-keep-falling
fit: adapted
status: rejected
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean strength of short-side drift-adjusted 18-bar return: 0.0246939; ordinary t: 1.52969 (threshold: confirm: mean > 0 with t >= 2; reject: mean < 0 with t <= -2; at least 30 cases)
- Supporting check: slope of drift-adjusted 18-bar return on 30-day return (t): -2.83833, passed: False
- Counts: cases: 3417, cases with 30-day return: 2481
- Decided by: Reject: the supporting slope has t <= -2 over at least 30 cases.
- Reading: The situation is the bar closing below the previous close while the 180-bar return recomputed from closes is below 0 (the recorded regime 'trending' where the 180 prior closes are not in the window), on the short side; cases are the first short bet of each 18-bar grid cell; the slope regresses the unscaled drift-adjusted return on the 30-day return pooled over coins, and its minimum of 30 cases applies to the cases that have a 30-day return.
- Size: unusual move +0.20 % per case over 18 bars, 0.025 of the coin's usual move (8.17 %); normal drift in its direction -0.41 %, total -0.21 %; 3417 cases
Plan: `steps_cards/03_test_plan/night4_exhaustion_run/plans/024-04_downrun-volume-fade-depth-rebound.b2_dips-in-downtrends-keep-falling_4h.md`
Record: `steps_cards/04_backtest/night4_exhaustion_run/backtests/024-04_downrun-volume-fade-depth-rebound.b2_dips-in-downtrends-keep-falling_4h`
Measure: `measure.py`
