---
plan: 058-01.g2.g1.d1.d2.e2_wide-bounce-two-day-fade_1d
idea: 058-01.g2.g1.d1.d2.e2_wide-bounce-two-day-fade
fit: exact
status: no effect
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 2-day move on the short side: -0.00595993; t of the mean, cases of one day taken together: -0.78637 (threshold: confirm: mean > 0 with t >= 2 (and supporting check passes); reject: mean < 0 with t <= -2)
- Supporting check: mean unusual move, upper half minus lower half of |forecast|: 0.00230809, passed: True
- Counts: cases: 361, distinct days: 199
- Decided by: t between -2 and 2: neither the confirm nor the reject rule is met (inconclusive rule). No effect (common/verdicts.md): t in the idea's direction -0.786 (below 1), 361 cases (30 needed).
- Reading: A case is the first short bet (forecast rising in size by at least 2 points from its lowest short level since the last bet) in each 2-bar grid cell from each window's first row, its 2-bar return taken from that bar's close inside the window; the drift is the coin's mean non-overlapping 2-bar return over all its windows; the t clusters cases by UTC day of the signal bar (with D/(D-1) correction); the upper half is |forecast| strictly above the median, the lower half at or below it.
- Size: unusual move -0.60 % (t -0.79, the cases of one day together: 199 days) per case over 2 bars, -0.088 of the coin's usual move (6.84 %); normal drift in its direction -0.12 %, total -0.72 %; 361 cases
- Effect check (common/verdicts.md): no effect: t in the idea's direction -0.786 (below 1), 361 cases (30 needed)
Plan: `steps_cards/03_test_plan/night10_fallagishort_run/plans/058-01.g2.g1.d1.d2.e2_wide-bounce-two-day-fade_1d.md`
Record: `steps_cards/04_backtest/night10_fallagishort_run/backtests/058-01.g2.g1.d1.d2.e2_wide-bounce-two-day-fade_1d`
Measure: `measure.py`
