---
plan: 002-05_sma-up-regime-positive-drift_1d
idea: 002-05_sma-up-regime-positive-drift
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean next-bar return in-stretch minus out-of-stretch: 0.00144308; Welch t: 0.698919 (threshold: confirm if difference > 0 with t >= 2; reject if difference < 0 with t <= -2; |t| < 2 inconclusive)
- Supporting check: share of up next-bars in-stretch minus out-of-stretch: -0.00109646, passed: False
- Counts: in-stretch bars: 290, out-of-stretch bars: 434, distinct up-cross stretches: 5
- Decided by: Welch t = 0.70 meets neither the confirm (t >= 2) nor the reject (t <= -2) rule.
- Reading: In-stretch bars are forecast > 0 and out-of-stretch bars forecast = 0, next-bar returns pooled over all windows; distinct up-cross stretches are counted as contiguous runs of raw SMA spread > 0 within each window (a run already open at a window's start counts); the plan's minimum counts, when unmet, give 'not observable'; the supporting check passes when the up-share difference is positive.
Plan: `steps_cards/03_test_plan/plans/002-05_sma-up-regime-positive-drift_1d.md`
Record: `steps_cards/04_backtest/backtests/002-05_sma-up-regime-positive-drift_1d`
Measure: `measure.py`
