---
plan: N3-02_breakout-shock-continues_1d
idea: N3-02_breakout-shock-continues
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess 5-bar forward return after shock-up new highs (forecast >= 10): 0.0107201; t of the mean: 2.03078 (threshold: mean > 0 with t >= 2 to confirm; mean < 0 with t <= -2 to reject)
- Supporting check: mean excess after new-high cases minus after inside-range shock-up days: 0.00645168, passed: True
- Counts: non-overlapping cases pooled across coins: 635, inside-range shock-up days: 1619
- Decided by: Mean excess 5-bar return is positive with t >= 2 and exceeds that after inside-range shock-up days.
- Reading: Coin mean is the mean of all overlapping 5-bar forward returns of the coin pooled over its windows; a signal at most 5 bars after the last kept case is merged into it; the standardised return is 10 x r / mean |r| of the last 60 one-day returns (min 20, current bar included, recomputed within each window); inside-range days are not merged; t is the ordinary t of the mean.
Plan: `steps_cards/03_test_plan/overnight_run/plans/N3-02_breakout-shock-continues_1d.md`
Record: `steps_cards/04_backtest/overnight_run/backtests/N3-02_breakout-shock-continues_1d`
Measure: `measure.py`
