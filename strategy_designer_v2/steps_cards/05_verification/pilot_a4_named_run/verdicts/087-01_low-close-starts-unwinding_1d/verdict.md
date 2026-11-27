---
plan: 087-01_low-close-starts-unwinding_1d
idea: 087-01_low-close-starts-unwinding
fit: exact
status: no effect
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 3-day move of short cases (drift removed, sign flipped): 0.00318978; t of the mean, cases clustered by day: 0.46085 (threshold: confirm: mean > 0 with t >= 2 over >= 30 case-days and check passes; reject: mean < 0 with t <= -2 over >= 30 case-days)
- Supporting check: mean unusual move, larger |forecast| half minus smaller half: 0.0202265, passed: True
- Counts: case-days: 240, cases: 331
- Decided by: The t lies between -2 and 2, meeting neither the confirm nor the reject rule. No effect (common/verdicts.md): t in the idea's direction +0.461 (below 1), 240 cases (30 needed).
- Reading: Situation checked as close location from the high (raw component, or recomputed from prices where not recorded) >= 0.8 with a short forecast, the profile being code-added and not rebuilt; a case is the first short bet (rise of |forecast| by >= 2 from its low since the last bet) in each 3-bar grid cell of a window with a full 3-bar return in it; drift is the coin's mean non-overlapping 3-bar return over all its windows; t is clustered by signal day; the median split puts |forecast| > median in the larger half.
- Size: unusual move +0.32 % (t 0.46, the cases of one day together: 240 days) per case over 3 bars, 0.031 of the coin's usual move (9.34 %); normal drift in its direction -0.39 %, total -0.07 %; 331 cases
- Effect check (common/verdicts.md): no effect: t in the idea's direction +0.461 (below 1), 240 cases (30 needed)
Plan: `steps_cards/03_test_plan/pilot_a4_named_run/plans/087-01_low-close-starts-unwinding_1d.md`
Record: `steps_cards/04_backtest/pilot_a4_named_run/backtests/087-01_low-close-starts-unwinding_1d`
Measure: `measure.py`
