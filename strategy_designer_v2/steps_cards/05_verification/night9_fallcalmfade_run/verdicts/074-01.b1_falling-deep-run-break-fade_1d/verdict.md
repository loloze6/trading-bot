---
plan: 074-01.b1_falling-deep-run-break-fade_1d
idea: 074-01.b1_falling-deep-run-break-fade
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: |forecast|-weighted mean drift-adjusted 1-bar short gain on forecast<0 bars: 0.00892257; t of weighted mean, day-clustered: 3.53519 (threshold: t >= 2 confirm, t <= -2 reject, over at least 100 cases)
- Supporting check: deeper-half minus shallower-half drift-adjusted next-day return <= 0: -0.00510758, passed: True
- Counts: cases: 1692, days: 739
- Decided by: Weighted mean gain t >= 2 over at least 100 cases and the deeper half's drift-adjusted return is not above the shallower half's.
- Reading: Situation from prices: up close after a down close, falling = 60-bar close change (percent) below -10, with run_depth raw > 0 and a non-chop regime used only where the window lacks the price lookback; t is the weighted mean over a day-clustered standard error (weighted deviations summed per day); halves split at the median |forecast| (deeper strictly above), compared by unweighted mean drift-adjusted next-day return.
- Size: unusual move +0.51 % (t 2.42, the cases of one day together: 642 days) per case over 1 bars, 0.109 of the coin's usual move (4.78 %); normal drift in its direction -0.12 %, total +0.39 %; 1429 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.004196 on the check folds against +0.008923 on every fold
Plan: `steps_cards/03_test_plan/night9_fallcalmfade_run/plans/074-01.b1_falling-deep-run-break-fade_1d.md`
Record: `steps_cards/04_backtest/night9_fallcalmfade_run/backtests/074-01.b1_falling-deep-run-break-fade_1d`
Measure: `measure.py`
