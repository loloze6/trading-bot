---
plan: N3-02_breakout-shock-continues_1d_oos2
idea: N3-02_breakout-shock-continues
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess 5-bar forward return after shock-up new-high cases (forecast >= 10): 0.0608044; one-sample t of the mean: 2.13086 (threshold: confirm if mean > 0 with t >= 2 (and supporting difference > 0); reject if mean < 0 with t <= -2; at least 30 non-overlapping cases)
- Supporting check: mean excess after new-high cases minus mean excess after inside-range shock-up days: 0.0776219, passed: True
- Counts: non-overlapping cases pooled across coins: 154, inside-range shock-up cases: 252
- Decided by: Mean excess 5-bar return is positive with t >= 2 and exceeds the inside-range shock-up mean excess, meeting the confirm rule.
- Reading: Signals are merged when they fall fewer than 5 bars after the last kept case in the same window (the same merge applied to the inside-range group), the coin's mean 5-bar return is the mean of all overlapping 5-bar forward returns of every bar in all its windows, the standardised return is 10 x the one-day return over the rolling mean absolute one-day return of the last 60 bars (min 20, within window), and the t is the ordinary one-sample t of the mean excess return.
Plan: `steps_cards/03_test_plan/overnight_run/plans_oos/N3-02_breakout-shock-continues_1d_oos2.md`
Record: `steps_cards/04_backtest/overnight_run/backtests_oos/N3-02_breakout-shock-continues_1d_oos2`
Measure: `measure.py`
