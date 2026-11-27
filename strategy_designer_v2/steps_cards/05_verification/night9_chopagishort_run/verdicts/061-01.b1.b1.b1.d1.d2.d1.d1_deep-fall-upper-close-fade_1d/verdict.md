---
plan: 061-01.b1.b1.b1.d1.d2.d1.d1_deep-fall-upper-close-fade_1d
idea: 061-01.b1.b1.b1.d1.d2.d1.d1_deep-fall-upper-close-fade
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 5-bar move of short cases, in the short's direction: 0.0316801; t of the mean, cases of one day pooled: 1.96128 (threshold: positive with t >= 2 to confirm; negative with t <= -2 to reject)
- Supporting check: top third minus bottom third by |forecast|, mean unusual move: -0.0167299, passed: False
- Counts: distinct case days: 99, cases: 139, active bars: 509
- Decided by: The t of the mean unusual move lies between -2 and 2.
- Reading: Profile part of the situation is read as the recorded regime not being 'chop' (its components are not recorded and the 365-bar volatility percentile cannot be rebuilt), each grid cell's case is its first bet bar, the day-pooled t uses a D/(D-1) cluster correction, thirds are floor(n/3) cases by |forecast|, and fewer than 30 distinct case days is reported as 'not observable' as the workflow's minimum-count rule asks.
- Size: unusual move +3.17 % (t 1.97, the cases of one day together: 99 days) per case over 5 bars, 0.303 of the coin's usual move (11.68 %); normal drift in its direction -0.65 %, total +2.52 %; 139 cases
Plan: `steps_cards/03_test_plan/night9_chopagishort_run/plans/061-01.b1.b1.b1.d1.d2.d1.d1_deep-fall-upper-close-fade_1d.md`
Record: `steps_cards/04_backtest/night9_chopagishort_run/backtests/061-01.b1.b1.b1.d1.d2.d1.d1_deep-fall-upper-close-fade_1d`
Measure: `measure.py`
