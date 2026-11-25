---
plan: 035-02_break-swings-above-continues_1d
idea: 035-02_break-swings-above-continues
fit: exact
status: not observable
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 5-day excess return over the coin's mean 5-day return, cases with forecast > 0: 0.0240836; t of the mean, cases of one day together: 1.0145 (threshold: confirm: mean > 0 with t >= 2 and Spearman > 0; reject: mean < 0 with t <= -2)
- Supporting check: Spearman correlation forecast vs 5-day excess return > 0: 0.100122, passed: True
- Counts: cases: 60, distinct days: 25, active bars: 241
- Decided by: The plan's minimum of 100 cases on at least 60 distinct days is not reached (60 cases, 25 days).
- Reading: Situation recomputed from prices as close above the max high of the 20 prior bars in the window (falling back to the recorded raw component > 0 on the first 20 bars), expected side long; cases are grid bars 0,5,10,... of each window with forecast > 0 and a 5-bar return inside the window; the coin's mean 5-day return is taken on the same non-overlapping grids of all its windows; the day-clustered t sums deviations per calendar day (UTC) with a D/(D-1) correction; the plan's minimum of 100 cases on 60 days, when not reached, gives 'not observable'.
- Size: unusual move +2.18 % (t 1.78, the cases of one day together: 78 days) per case over 5 bars, 0.171 of the coin's usual move (9.44 %); normal drift in its direction +0.33 %, total +2.51 %; 144 cases
Plan: `steps_cards/03_test_plan/night7_rangefail_run/plans/035-02_break-swings-above-continues_1d.md`
Record: `steps_cards/04_backtest/night7_rangefail_run/unseen_2026/backtests/035-02_break-swings-above-continues_1d`
Measure: `measure.py`
