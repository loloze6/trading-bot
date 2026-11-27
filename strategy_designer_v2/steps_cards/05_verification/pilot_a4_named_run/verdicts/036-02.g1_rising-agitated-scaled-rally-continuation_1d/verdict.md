---
plan: 036-02.g1_rising-agitated-scaled-rally-continuation_1d
idea: 036-02.g1_rising-agitated-scaled-rally-continuation
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 3-day move after bet bars: 0.0166875; t of the mean, same-day cases pooled: 1.61524 (threshold: confirm: mean > 0 with t >= 2 and positive slope; reject: mean < 0 with t <= -2)
- Supporting check: OLS slope of unusual move on forecast: 0.0016182, passed: True
- Counts: distinct case days: 193, cases: 240
- Decided by: t is between -2 and 2.
- Reading: Situation = scaled rise >= 1.0 from the recorded scaled_rise raw value (recomputed from prices where missing) on bars the detector labelled trending, since the profile components are not recorded and the regime carries their vetoes; side long; a case is the first bet bar (long-side forecast rise >= 2 from its lowest level since the last bet) in each 3-bar grid cell of a window, t pools same-day deviations with a G/(G-1) cluster correction, and fewer than 30 distinct case days gives not observable.
- Size: unusual move +1.67 % (t 1.62, the cases of one day together: 193 days) per case over 3 bars, 0.176 of the coin's usual move (9.34 %); normal drift in its direction +0.36 %, total +2.03 %; 240 cases
- Effect check (common/verdicts.md): unclear: t in the idea's direction +1.615 (not below 1), 193 cases (30 needed)
Plan: `steps_cards/03_test_plan/pilot_a4_named_run/plans/036-02.g1_rising-agitated-scaled-rally-continuation_1d.md`
Record: `steps_cards/04_backtest/pilot_a4_named_run/backtests/036-02.g1_rising-agitated-scaled-rally-continuation_1d`
Measure: `measure.py`
