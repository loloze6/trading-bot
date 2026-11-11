---
plan: 002-05_sma-up-regime-positive-drift_1d_none
idea: 002-05_sma-up-regime-positive-drift
fit: adapted
status: inconclusive
---
Situation check: 1 of the active bars match the plan's situation and side
Evidence:
- Main measure: mean next-bar return in-stretch minus out-of-stretch: 0.00144308; Welch t: 0.698919 (threshold: confirm if difference > 0 with Welch t >= 2; reject if difference < 0 with t <= -2; else inconclusive; needs >= 100 in, >= 100 out, >= 3 stretches)
- Supporting check: share of up next-bars in-stretch minus out-of-stretch: -0.00109646, passed: False
- Counts: in-stretch bars: 290, out-of-stretch bars: 434, distinct up-cross stretches: 5
- Decided by: Inconclusive: |t| < 2 for the in-stretch minus out-of-stretch mean next-bar return.
- Reading: In-stretch bars are forecast > 0 and out-of-stretch bars forecast = 0 with next-bar returns taken inside each window; the situation is a positive raw SMA spread with a long forecast; a distinct up-cross stretch is a contiguous run of positive raw spread within one window; the supporting check passes when its difference is positive.
Plan: `steps_cards/05_verification/planted_test/plans/002-05_sma-up-regime-positive-drift_1d_none.md`
Record: `steps_cards/05_verification/planted_test/records/002-05_sma-up-regime-positive-drift_1d_none`
Measure: `measure.py`
