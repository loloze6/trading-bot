---
plan: 002-05_sma-up-regime-positive-drift_1d_plus0.1pct
idea: 002-05_sma-up-regime-positive-drift
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: in-stretch minus out-of-stretch mean next-bar return: 0.00244308; Welch t: 1.18324 (threshold: confirm if positive with Welch t >= 2; reject if negative with t <= -2; else inconclusive (needs >=100 in, >=100 out, >=3 stretches))
- Supporting check: share of up next-bars in-stretch minus out-of-stretch: 0.0506277, passed: True
- Counts: in-stretch bars: 290, out-of-stretch bars: 434, distinct up-cross stretches: 5
- Decided by: |t| < 2, so the result is inconclusive.
- Reading: In-stretch bars are forecast > 0 and out-of-stretch bars are forecast = 0, with every bar that has a next close in the same window pooled across windows. Distinct up-cross stretches are maximal runs of forecast > 0 within each window. The supporting check passes when its value is above zero.
Plan: `steps_cards/05_verification/planted_test/plans/002-05_sma-up-regime-positive-drift_1d_plus0.1pct.md`
Record: `steps_cards/05_verification/planted_test/records/002-05_sma-up-regime-positive-drift_1d_plus0.1pct`
Measure: `measure.py`
