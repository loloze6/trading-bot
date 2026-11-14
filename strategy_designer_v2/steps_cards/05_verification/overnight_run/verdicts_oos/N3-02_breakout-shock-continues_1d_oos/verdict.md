---
plan: N3-02_breakout-shock-continues_1d_oos
idea: N3-02_breakout-shock-continues
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess 5-bar return after shock-up new-high cases (forecast >= 10), before costs: 0.0111353; t of the mean: 1.67844 (threshold: confirm if mean > 0 with t >= 2 (and supporting difference > 0); reject if mean < 0 with t <= -2)
- Supporting check: mean excess after new-high cases minus mean excess after inside-range shock-up days: 0.0129563, passed: True
- Counts: non-overlapping cases pooled across coins: 447, inside-range shock-up cases: 809
- Decided by: t lies between -2 and 2, which the plan calls inconclusive.
- Reading: Situation recomputed from closes as close >= max of current and prior 20 closes within each window (regime=='trending' used where fewer than 21 bars exist) plus a positive one-day return, side long; the coin baseline is the mean of all bars' 5-bar forward returns pooled across its windows; signals within 5 bars (distance <= 5) of the last kept case are merged into it, the case being its first bar, and the same merging is applied to the inside-range group; the standardised return is 10 x r / mean|r| over the last 60 one-day returns including the current one (min 20); t is the ordinary t of the mean.
Plan: `steps_cards/03_test_plan/overnight_run/plans_oos/N3-02_breakout-shock-continues_1d_oos.md`
Record: `steps_cards/04_backtest/overnight_run/backtests_oos/N3-02_breakout-shock-continues_1d_oos`
Measure: `measure.py`
