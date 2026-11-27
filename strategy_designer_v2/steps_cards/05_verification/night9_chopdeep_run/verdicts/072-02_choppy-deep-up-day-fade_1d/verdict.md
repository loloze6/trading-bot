---
plan: 072-02_choppy-deep-up-day-fade_1d
idea: 072-02_choppy-deep-up-day-fade
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: depth-weighted short gain vs holding, next day, mean per case: 0.00285519; t of the mean over per-day sums: 1.86848 (threshold: confirm if t >= 2 with check < 0; reject if t <= -2)
- Supporting check: deepest third minus shallowest third, mean excess next-day return: 1.83668e-06, passed: False
- Counts: cases: 1691, distinct days: 1028
- Decided by: The main-measure t is between -2 and 2.
- Reading: Choppy is read as the 60-bar close-to-close return within -10 % and +10 % (the config's veto bounds), an up day as a 1-bar return above 0 and the depth as the raw component below 0, with active bars whose 60-bar return cannot be computed inside the window left out of the agreement share; the main value is the per-case mean and its t is the ordinary t over the per-day sums of the cases; thirds are cut on the cases sorted by post_pipeline_value (most negative = deepest) into three near-equal groups.
- Size: unusual move +0.22 % (t 1.47, the cases of one day together: 691 days) per case over 1 bars, 0.057 of the coin's usual move (4.78 %); normal drift in its direction -0.12 %, total +0.11 %; 1041 cases
Plan: `steps_cards/03_test_plan/night9_chopdeep_run/plans/072-02_choppy-deep-up-day-fade_1d.md`
Record: `steps_cards/04_backtest/night9_chopdeep_run/backtests/072-02_choppy-deep-up-day-fade_1d`
Measure: `measure.py`
