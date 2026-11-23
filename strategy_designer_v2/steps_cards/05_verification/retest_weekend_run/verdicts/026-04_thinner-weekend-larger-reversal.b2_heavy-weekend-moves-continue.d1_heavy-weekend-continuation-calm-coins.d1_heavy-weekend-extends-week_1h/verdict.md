---
plan: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins.d1_heavy-weekend-extends-week_1h
idea: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins.d1_heavy-weekend-extends-week
fit: exact
status: confirmed
---
Situation check: 92 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean signed excess 48-bar return: 0.0185333; t of the mean: 3.1061 (threshold: confirm: mean > 0 with t >= 2 (and rank correlation > 0); reject: mean < 0 with t <= -2)
- Supporting check: Spearman of abs(forecast) vs signed excess return: 0.0653634, passed: True
- Counts: cases: 284
- Decided by: The mean signed excess return is above 0 with t >= 2 and the rank correlation is above 0.
- Reading: The Monday 00:00 case bar is the bar closing at Monday 00:00 UTC, accepted as the bar stamped Sunday 23:00 or Monday 00:00 because the record's timestamp convention may differ, with the situation computed from prices on that bar (48-bar return, 120-bar return ending 48 bars earlier, mean volume of the last 48 bars over bars t-167..t-48), and the coin's mean 48-bar return is taken on the non-overlapping 48-bar grid of all its windows pooled.
- Size: unusual move +1.74 % per case over 48 bars, 0.243 of the coin's usual move (6.56 %); normal drift in its direction +0.08 %, total +1.82 %; 277 cases
Plan: `steps_cards/03_test_plan/retest_weekend_run/plans/026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins.d1_heavy-weekend-extends-week_1h.md`
Record: `steps_cards/04_backtest/retest_weekend_run/backtests/026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins.d1_heavy-weekend-extends-week_1h`
Measure: `measure.py`
