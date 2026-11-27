---
plan: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins.d2_heavy-weekend-monday-morning-continuation.d2_heavy-weekend-falls-continue_1h
idea: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins.d2_heavy-weekend-monday-morning-continuation.d2_heavy-weekend-falls-continue
fit: exact
status: confirmed
---
Situation check: 99 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-direction 12-bar excess return over coin drift, Sunday 23:00 signals (forecast <= -2): 0.0165699; ordinary t of the mean: 5.1638 (threshold: confirm: t >= 2 with slope on forecast size > 0; reject: t <= -2; otherwise inconclusive; at least 30 cases)
- Supporting check: least-squares slope of short-direction excess return on |forecast|: 0.00122958, passed: True
- Counts: cases over all coins and windows: 316
- Decided by: Mean short-direction excess return is positive with t >= 2 and the slope on the forecast's size is above 0.
- Reading: Situation bars are those starting Sunday 23:00 UTC with a negative raw weekend_fall value (else negative 48-bar return) and a recomputed 48/120-bar volume ratio above 1 (regime 'trending' where it cannot be recomputed); the excess is -(r12 - coin drift), drift being the coin's mean 12-bar return on the 0,12,24,... grid of all its windows; cases are deduplicated to the first per coin and ISO week, those without 12 later bars in the window are dropped, and the slope is on |forecast|.
- Size: unusual move +1.66 % (t 2.05, the cases of one day together: 136 days) per case over 12 bars, 0.397 of the coin's usual move (3.89 %); normal drift in its direction -0.11 %, total +1.55 %; 316 cases
- Direction check on folds A, D (the years step 7 does not explore): not judged: no check fold (the plan has none, or the backtest did not run on its folds)
Plan: `steps_cards/03_test_plan/retest_weekend_run/plans/026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins.d2_heavy-weekend-monday-morning-continuation.d2_heavy-weekend-falls-continue_1h.md`
Record: `steps_cards/04_backtest/retest_weekend_run/common/backtests/026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins.d2_heavy-weekend-monday-morning-continuation.d2_heavy-weekend-falls-continue_1h`
Measure: `measure.py`
