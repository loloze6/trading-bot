---
plan: 002-05_sma-up-regime-positive-drift_1d
idea: 002-05_sma-up-regime-positive-drift
fit: adapted
status: not observable
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: in-stretch minus out-of-stretch mean next-bar return: -0.00690032; Welch t: -0.950719 (threshold: confirm if difference > 0 with Welch t >= 2; reject if difference < 0 with t <= -2; otherwise inconclusive)
- Supporting check: share of up next-bars in-stretch minus out-of-stretch: -0.134253, passed: False
- Counts: in-stretch bars: 13, out-of-stretch bars: 106, up-cross stretches: 1
- Decided by: The plan's minimum counts are not reached: in-stretch bars 13 < 100; up-cross stretches 1 < 3.
- Reading: In-stretch bars are bars with forecast > 0 and out-of-stretch bars those with forecast = 0, each with its next-bar return inside its own window pooled over all windows present; distinct up-cross stretches are counted as contiguous runs of the raw SMA50-SMA200 spread above zero in each window (a run already under way at the window's start counts as one); the supporting check passes when the up-share difference is positive; the plan's minimum counts, when unmet, give 'not observable'.
Plan: `steps_cards/05_verification/exercise_11/plans/002-05_sma-up-regime-positive-drift_1d.md`
Record: `steps_cards/05_verification/exercise_11/records/002-05_sma-up-regime-positive-drift_1d`
Measure: `measure.py`
