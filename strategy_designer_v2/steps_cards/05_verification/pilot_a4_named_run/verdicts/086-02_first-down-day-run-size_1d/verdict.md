---
plan: 086-02_first-down-day-run-size_1d
idea: 086-02_first-down-day-run-size
fit: exact
status: no effect
---
Situation check: 99 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-direction unusual move over 3 bars (vs coin's normal 3-bar drift): -0.00817561; t of the mean, cases summed by day: -1.16518 (threshold: confirm: mean > 0 with day-clustered t >= 2; reject: mean < 0 with t <= -2)
- Supporting check: OLS slope of unusual move on |forecast|: -0.00138888, passed: False
- Counts: cases: 465, distinct days: 341
- Decided by: Inconclusive rule: the results lie between the confirm and reject rules. No effect (common/verdicts.md): t in the idea's direction -1.165 (below 1), 465 cases (30 needed).
- Reading: Situation = regime 'trending' (the detector's decision, which carries the rising-agitated profile whose 365-bar volatility percentile cannot be rebuilt inside the recorded windows) on a down close with the recorded run gain > 0 (recomputed from prices where not recorded), expected side short; cases are short bets (short size up >= 2 from its lowest since the last bet), first one per 3-bar grid cell of each window; drift is the coin's mean 3-bar return on that grid over all its windows; the day-clustered t sums case deviations per UTC day; the slope t is ordinary least squares; the plan's 'fewer than 30 cases or 30 days' minimum is reported as not observable.
- Size: unusual move -0.82 % (t -1.17, the cases of one day together: 341 days) per case over 3 bars, -0.098 of the coin's usual move (9.34 %); normal drift in its direction -0.37 %, total -1.19 %; 465 cases
- Effect check (common/verdicts.md): no effect: t in the idea's direction -1.165 (below 1), 465 cases (30 needed)
Plan: `steps_cards/03_test_plan/pilot_a4_named_run/plans/086-02_first-down-day-run-size_1d.md`
Record: `steps_cards/04_backtest/pilot_a4_named_run/backtests/086-02_first-down-day-run-size_1d`
Measure: `measure.py`
