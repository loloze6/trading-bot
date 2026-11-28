---
plan: 086-02_first-up-after-deep-down-run_1d
idea: 086-02_first-up-after-deep-down-run
fit: adapted
status: no effect
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 5-day excess return of trending cases with forecast > 0 (vs coin's mean 5-day return): -0.00131417; t of the mean, same-day cases summed: -0.15649 (threshold: confirm: mean > 0 with t >= 2 (day-clustered); reject: t <= -2)
- Supporting check: OLS slope of 5-day excess return on depth last_history_value (t): -2.16166, passed: False
- Counts: independent case-days: 262, cases: 390
- Decided by: Reject rule: the mean excess 5-day return has t <= -2 or the depth slope has t <= -2. No effect (common/verdicts.md): the plan's reject rule is met.
- Reading: Situation rebuilt from closes (up close after >= 2 lower closes) on bars with regime 'trending' (the profile vetoes cannot be recomputed in-window, so their pass is read from the regime, and the first 3 bars of a window use depth > 0); a case is the first trending bar with forecast > 0 in each 5-bar grid cell of its window, its return taken from that bar's close over 5 bars inside the window; the coin's mean is over all its windows' non-overlapping grid returns; the plan's '< 30 case-days' minimum is reported as 'not observable'.
- Size: unusual move -0.11 % (t -0.13, the cases of one day together: 261 days) per case over 5 bars, -0.028 of the coin's usual move (11.39 %); normal drift in its direction +0.65 %, total +0.54 %; 389 cases
- Effect check (common/verdicts.md): no effect: the plan's reject rule is met
Plan: `steps_cards/03_test_plan/night10_riseagilong_run/plans/086-02_first-up-after-deep-down-run_1d.md`
Record: `steps_cards/04_backtest/night10_riseagilong_run/backtests/086-02_first-up-after-deep-down-run_1d`
Measure: `measure.py`
