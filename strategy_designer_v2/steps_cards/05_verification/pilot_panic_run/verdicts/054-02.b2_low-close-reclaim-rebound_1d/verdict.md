---
plan: 054-02.b2_low-close-reclaim-rebound_1d
idea: 054-02.b2_low-close-reclaim-rebound
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 5-day move (return minus coin's normal 5-day drift): 0.0294914; t of the mean, same-day cases pooled: 1.55016 (threshold: confirm: mean > 0 with t >= 2; reject: t <= -2)
- Supporting check: above-median minus below-median forecast mean unusual move (Welch t): 0.0475134, passed: True
- Counts: cases: 75, days: 49, cases above median: 37, cases below median: 37
- Decided by: The mean unusual move's t lies between -2 and 2 (or is not measurable): inconclusive rule.
- Reading: Situation computed as low[t] < min(low[t-30..t-1]) < close[t] inside each window, active bars lacking 30 prior bars in their window left out of the check; a case is the first bet (forecast rise of >= 2 points from its lowest level on its side since the last bet, from 0 after flat) in each 5-bar grid cell of a window, its return taken from that bet's close over 5 bars within the window; the coin's normal drift is the mean of its non-overlapping 5-bar grid returns over all windows; the supporting split uses forecast strictly above vs strictly below the cases' median forecast; the main t clusters cases by UTC day.
- Size: unusual move +2.95 % (t 1.57, the cases of one day together: 49 days) per case over 5 bars, 0.273 of the coin's usual move (10.60 %); normal drift in its direction +0.64 %, total +3.59 %; 75 cases
Plan: `steps_cards/03_test_plan/pilot_panic_run/plans/054-02.b2_low-close-reclaim-rebound_1d.md`
Record: `steps_cards/04_backtest/pilot_panic_run/backtests/054-02.b2_low-close-reclaim-rebound_1d`
Measure: `measure.py`
