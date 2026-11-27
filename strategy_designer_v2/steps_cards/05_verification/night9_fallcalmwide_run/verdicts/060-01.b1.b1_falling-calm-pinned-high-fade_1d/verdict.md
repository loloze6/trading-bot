---
plan: 060-01.b1.b1_falling-calm-pinned-high-fade_1d
idea: 060-01.b1.b1_falling-calm-pinned-high-fade
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 1-bar move in the short direction, before costs: 0.00399199; t of the mean, cases of one day together: 0.857849 (threshold: confirm: mean > 0 with t >= 2 over >= 30 cases and check passes; reject: mean < 0 with t <= -2 over >= 30 cases)
- Supporting check: unusual move of cases closer to the high minus the others (split at median high_gap) >= 0: 0.00944982, passed: True
- Counts: cases: 124, days: 82
- Decided by: t between -2 and 2 (or not computable) over at least 30 cases.
- Reading: Situation checked as width>=2.0 (range/close over the 30-bar ddof-1 std of daily returns, including the bar) and close location from the low>=0.9, on the short side, leaving the falling-calm profile to the engine and excluding active bars with under 30 in-window returns; the coin's normal drift is its mean 1-bar return over all its windows; the day-clustered t uses per-day summed deviations with a D/(D-1) correction; 'closer to the high' means high_gap at or below the median of the cases, 'the others' above it.
- Size: unusual move +0.42 % (t 0.90, the cases of one day together: 81 days) per case over 1 bars, 0.081 of the coin's usual move (5.33 %); normal drift in its direction -0.13 %, total +0.29 %; 122 cases
Plan: `steps_cards/03_test_plan/night9_fallcalmwide_run/plans/060-01.b1.b1_falling-calm-pinned-high-fade_1d.md`
Record: `steps_cards/04_backtest/night9_fallcalmwide_run/backtests/060-01.b1.b1_falling-calm-pinned-high-fade_1d`
Measure: `measure.py`
