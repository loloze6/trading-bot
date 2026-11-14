---
plan: 002-05_sma-up-regime-positive-drift_1d_minus1pct
idea: 002-05_sma-up-regime-positive-drift
fit: adapted
status: rejected
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean next-bar return in-stretch minus out-of-stretch: -0.00855692; Welch t: -4.14431 (threshold: confirm if difference > 0 with Welch t >= 2; reject if difference < 0 with t <= -2; else inconclusive; needs >= 100 in-stretch bars, >= 100 out-of-stretch bars, >= 3 distinct up-cross stretches)
- Supporting check: share of up next-bars in-stretch minus out-of-stretch: -0.204545, passed: False
- Counts: in-stretch bars: 290, out-of-stretch bars: 434, distinct up-cross stretches: 5
- Decided by: The difference is negative with t <= -2, so moves after up crosses reverse.
- Reading: Distinct up-cross stretches are counted as contiguous runs of raw spread > 0 within each window, a run starting at a window's first row included. The supporting check passes when its difference is > 0.
Plan: `steps_cards/05_verification/planted_test/plans/002-05_sma-up-regime-positive-drift_1d_minus1pct.md`
Record: `steps_cards/05_verification/planted_test/records/002-05_sma-up-regime-positive-drift_1d_minus1pct`
Measure: `measure.py`
