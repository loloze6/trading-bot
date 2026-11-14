---
plan: 002-05_sma-up-regime-positive-drift_1d
idea: 002-05_sma-up-regime-positive-drift
fit: adapted
status: not observable
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: in-stretch minus out-of-stretch mean next-bar return: -0.00690032; Welch t: -0.950719 (threshold: confirm if difference > 0 with Welch t >= 2; reject if < 0 with t <= -2; else inconclusive)
- Supporting check: share of up next-bars in-stretch minus out-of-stretch: -0.134253, passed: False
- Counts: in-stretch bars: 13, out-of-stretch bars: 106, distinct up-cross stretches: 1
- Decided by: Minimum count not reached: 13 in-stretch bars < 100; 1 up-cross stretches < 3.
- Reading: In-stretch bars are forecast > 0 and out-of-stretch bars forecast = 0, every bar's next-bar return counted once within its window; distinct up-cross stretches are counted as separate runs of raw SMA spread > 0 in each window (a run already under way at a window's start counts); the plan's 'inconclusive with fewer cases' is reported as 'not observable' per the minimum-count rule.
Plan: `steps_cards/05_verification/exercise_11/plans/002-05_sma-up-regime-positive-drift_1d.md`
Record: `steps_cards/05_verification/exercise_11/records/002-05_sma-up-regime-positive-drift_1d`
Measure: `measure.py`
