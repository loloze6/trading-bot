---
plan: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d2_trend-aligned-heavy-weekend-continuation_1h
idea: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d2_trend-aligned-heavy-weekend-continuation
fit: exact
status: inconclusive
---
Situation check: 99 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean signed unusual 48-bar move per case: 0.010387; t of the mean: 1.76018 (threshold: mean > 0 with t >= 2 (and check passes) to confirm; mean < 0 with t <= -2 to reject)
- Supporting check: top-half minus bottom-half |forecast| mean unusual move: 0.0143395, passed: True
- Counts: cases: 258
- Decided by: t lies between -2 and 2.
- Reading: Situation bar = bar starting Sunday 23:00 UTC with volume ratio (mean of last 48 bars over the mean of the 120 before) >= 1 and weekend-return sign equal to the recorded trend30d sign, expected side = weekend move sign; active bars whose values cannot be computed are left out of the agreement; the 'fewer than 100 cases' rule is applied as 'not observable'; top/bottom half pool all cases ranked by |forecast| (middle case dropped if odd).
- Size: unusual move +1.07 % per case over 48 bars, 0.150 of the coin's usual move (6.56 %); normal drift in its direction +0.07 %, total +1.14 %; 252 cases
Plan: `steps_cards/03_test_plan/retest_weekend_run/plans/026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d2_trend-aligned-heavy-weekend-continuation_1h.md`
Record: `steps_cards/04_backtest/retest_weekend_run/backtests/026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d2_trend-aligned-heavy-weekend-continuation_1h`
Measure: `measure.py`
