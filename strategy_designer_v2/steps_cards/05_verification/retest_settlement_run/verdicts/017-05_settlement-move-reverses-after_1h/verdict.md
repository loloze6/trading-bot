---
plan: 017-05_settlement-move-reverses-after_1h
idea: 017-05_settlement-move-reverses-after
fit: exact
status: confirmed
---
Situation check: 99 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of forecast/10 x drift-removed 2-bar return per case: 0.000438208; ordinary t of the mean: 5.11781 (threshold: t >= 2 (with supporting check) confirms; t <= -2 rejects; otherwise inconclusive)
- Supporting check: Welch t of top-third minus bottom-third |forecast| drift-removed return in forecast direction: 2.47725, passed: True
- Counts: cases: 51399, top third cases: 17133, bottom third cases: 17133
- Decided by: Confirm: the main measure has t >= 2 and the supporting check passes (Welch t >= 2).
- Reading: A settlement bar is a bar whose close (start + 1h) falls at 00:00, 08:00 or 16:00 UTC and the expected side is opposite to the 2-bar pre-move (recorded raw value, else rebuilt from closes); the coin's normal 2-bar drift is the mean of non-overlapping 2-bar returns (grid 0,2,4,... per window, inside windows) pooled over all the coin's windows; thirds are taken over all cases pooled, sorted by |forecast| (n//3 lowest vs n//3 highest); the plan's 1000-case minimum, when missed, gives 'not observable' as the workflow requires.
- Size: unusual move +0.05 % per case over 2 bars, 0.032 of the coin's usual move (1.47 %); normal drift in its direction -0.00 %, total +0.05 %; 44171 cases
Plan: `steps_cards/03_test_plan/retest_settlement_run/plans/017-05_settlement-move-reverses-after_1h.md`
Record: `steps_cards/04_backtest/retest_settlement_run/backtests/017-05_settlement-move-reverses-after_1h`
Measure: `measure.py`
