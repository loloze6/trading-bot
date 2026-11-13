---
plan: N5-02_high-below-60-day-fails_1d
idea: N5-02_high-below-60-day-fails
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 7-bar excess return of the coin after forecast <= -10 over its mean 7-bar return: 0.0101162; t of the mean: 1.26436 (threshold: confirm: mean < 0 with t <= -2 and share negative > 50%; reject: mean > 0 with t >= +2; at least 30 non-overlapping cases)
- Supporting check: share of cases with negative 7-bar excess return over holding: 0.492308, passed: False
- Counts: non-overlapping cases: 195
- Decided by: Inconclusive rule: t lies between -2 and +2.
- Reading: Non-overlapping cases are the grid bars at positions 0, 7, 14, ... of each window where forecast <= -10 and the bar 7 later is in the window. The coin's mean 7-bar return is taken on the same grid over all its windows. The excess over holding in the supporting check is that same return minus the coin mean. The 30-case minimum, if not reached, gives 'not observable'.
Plan: `steps_cards/03_test_plan/overnight_run/plans/N5-02_high-below-60-day-fails_1d.md`
Record: `steps_cards/04_backtest/overnight_run/backtests/N5-02_high-below-60-day-fails_1d`
Measure: `measure.py`
