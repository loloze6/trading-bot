---
plan: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b2_broken-support-ten-day-fall.c2_broken-support-in-downtrend_1d
idea: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b2_broken-support-ten-day-fall.c2_broken-support-in-downtrend
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: |forecast|-weighted mean of short-direction 10-bar excess return (return minus drift, x -1): 0.0179426; t of the |forecast|-weighted mean (effective n): 2.96471 (threshold: confirm: weighted mean > 0 with t >= 2 and supporting check > 0; reject: weighted mean < 0 with t <= -2)
- Supporting check: mean short excess return, larger-|forecast| half minus smaller half: 0.0192174, passed: True
- Counts: cases: 809
- Decided by: the weighted mean is above 0 with t >= 2 and the larger-|forecast| half beats the smaller half.
- Reading: the situation is a 60-day return below 0 (recomputed from the window's closes, the recorded regime where fewer than 60 past closes exist) with a positive raw cluster value (a swing low above the close), on the short side; cases are grid bars 0,10,20,... of each window with a full 10-bar return inside it, the drift is the coin's mean grid 10-bar return over all windows, the t is the weighted mean over its weighted standard error with Kish effective n, and the halves are the top and bottom n//2 cases by |forecast| (middle case dropped when odd) compared by unweighted means.
- Size: unusual move +0.58 % per case over 10 bars, 0.043 of the coin's usual move (14.49 %); normal drift in its direction -1.19 %, total -0.61 %; 901 cases
Plan: `steps_cards/03_test_plan/night3_levels_run/plans/020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b2_broken-support-ten-day-fall.c2_broken-support-in-downtrend_1d.md`
Record: `steps_cards/04_backtest/night3_levels_run/backtests/020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b2_broken-support-ten-day-fall.c2_broken-support-in-downtrend_1d`
Measure: `measure.py`
