---
plan: N1-02_above-rising-long-average_1d
idea: N1-02_above-rising-long-average
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 20-bar forward log return on forecast>0 bars minus mean over all bars (holding): -0.000889002; Welch t, non-overlapping 20-bar blocks: 0.0587253 (threshold: confirm if excess > 0 with t >= 2; reject if excess < 0 with t <= -2; otherwise inconclusive)
- Supporting check: OLS slope of 20-bar forward log return on forecast, active bars: 0.00344593, passed: True
- Counts: non-overlapping 20-bar active cases: 326, non-overlapping 20-bar holding cases: 811, active bars: 5738
- Decided by: The t-statistic lies between -2 and 2 (or disagrees in sign with the excess), meeting neither rule.
- Reading: The SMA200 is rebuilt from the close and the raw distance (taken as percent if its median absolute value exceeds 1, else as a fraction) and its 20-bar slope is checked only on active bars at least 20 rows into their window; the main value pools all bars (overlapping) while its t is Welch's t between active and all bars on the 0,20,40,... grid of each window; the plan's '<30 non-overlapping active cases' rule is reported as not observable; the supporting slope uses 20-bar forward log returns on all active bars.
Plan: `steps_cards/03_test_plan/overnight_run/plans_newcomp/N1-02_above-rising-long-average_1d.md`
Record: `steps_cards/04_backtest/overnight_run/backtests/N1-02_above-rising-long-average_1d`
Measure: `measure.py`
