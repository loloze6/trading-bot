---
plan: 060-02_falling-calm-low-to-close-fade_1d
idea: 060-02_falling-calm-low-to-close-fade
fit: adapted
status: no effect
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean next-day unusual move, signed for the short, before costs: 0.00139271; t of the mean, cases grouped by day: 0.276284 (threshold: positive with t >= 2 to confirm; negative with t <= -2 to reject)
- Supporting check: upper-half minus lower-half mean unusual move (split at raw lift median): 0.0038504, passed: True
- Counts: distinct case days: 104, cases: 161
- Decided by: The t of the mean unusual move lies between -2 and 2. No effect (common/verdicts.md): t in the idea's direction +0.276 (below 1), 104 cases (30 needed).
- Reading: Situation = recorded raw lift (recomputed from prices if missing) >= 2.0 on bars where the regime detector chose mean_reversion (its vetoes are the falling-calm profile, whose 60- and 365-bar inputs cannot be rebuilt inside a window), expected side short; cases = every bar with forecast < 0 that has a next bar in its window; drift = coin's mean 1-bar return over all its windows; t clusters deviations by UTC day; supporting split: upper = raw lift strictly above the cases' median, lower = at or below.
- Size: unusual move +0.18 % (t 0.36, the cases of one day together: 98 days) per case over 1 bars, 0.043 of the coin's usual move (4.83 %); normal drift in its direction -0.04 %, total +0.14 %; 150 cases
- Effect check (common/verdicts.md): no effect: t in the idea's direction +0.276 (below 1), 104 cases (30 needed)
Plan: `steps_cards/03_test_plan/pilot_a4_auto_run/plans/060-02_falling-calm-low-to-close-fade_1d.md`
Record: `steps_cards/04_backtest/pilot_a4_auto_run/backtests/060-02_falling-calm-low-to-close-fade_1d`
Measure: `measure.py`
