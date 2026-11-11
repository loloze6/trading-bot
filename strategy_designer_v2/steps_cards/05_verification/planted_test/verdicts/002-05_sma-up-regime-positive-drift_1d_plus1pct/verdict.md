---
plan: 002-05_sma-up-regime-positive-drift_1d_plus1pct
idea: 002-05_sma-up-regime-positive-drift
fit: adapted
status: confirmed
---
Situation check: 1 of the active bars match the plan's situation and side
Evidence:
- Main measure: in-stretch minus out-of-stretch mean next-bar return: 0.0114431; Welch t: 5.54215 (threshold: confirm if positive with Welch t >= 2; reject if negative with Welch t <= -2; else inconclusive)
- Supporting check: share of up next-bars in-stretch minus out-of-stretch: 0.281662, passed: True
- Counts: in-stretch bars: 290, out-of-stretch bars: 434, distinct up-cross stretches: 5
- Decided by: The in-stretch minus out-of-stretch mean next-bar return is positive with t >= 2.
- Reading: Situation is the raw SMA spread > 0 on long bars. In-stretch means forecast > 0 and out-of-stretch means forecast = 0, pooled over all windows with one next-bar return per bar inside its window. A distinct up-cross stretch is a contiguous run of forecast > 0 bars within one window, and a run already open at the window's start counts. 'Up' means a next-bar return > 0, and the supporting check passes if the difference in up shares is > 0.
Plan: `steps_cards/05_verification/planted_test/plans/002-05_sma-up-regime-positive-drift_1d_plus1pct.md`
Record: `steps_cards/05_verification/planted_test/records/002-05_sma-up-regime-positive-drift_1d_plus1pct`
Measure: `measure.py`
