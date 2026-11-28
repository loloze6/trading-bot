---
plan: 047-02_falling-agitated-scaled-rise-fade_1d
idea: 047-02_falling-agitated-scaled-rise-fade
fit: exact
status: no effect
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 3-bar move per short case (signed short): -0.000734573; day-clustered t: -0.143119 (threshold: confirm: mean > 0 with day-clustered t >= 2 and check passed; reject: mean < 0 with day-clustered t <= -2)
- Supporting check: mean unusual move (forecast <= -10) minus (0 > forecast > -10): 0.0207402, passed: True
- Counts: days with cases: 316, cases: 617, cases forecast <= -10: 247, cases 0 > forecast > -10: 370
- Decided by: The day-clustered t lies between -2 and 2. No effect (common/verdicts.md): t in the idea's direction -0.143 (below 1), 247 cases (30 needed).
- Reading: The situation is an up day (raw scaled rise > 0, or the day's close-to-close return when the raw value is not recorded) with a short forecast; a case is the first short bet (forecast falling >= 2 points below its least-short level since the last bet, reset at flat) in each 3-bar grid cell from each window's first row, with a full 3-bar return inside the window; the drift is each coin's mean non-overlapping 3-bar return over all its windows; the day-clustered t uses per-day summed deviations with a G/(G-1) correction; the plan's 'fewer than 30 days' rule is reported as not observable; an empty forecast group makes the check fail.
- Size: unusual move -0.07 % (t -0.14, the cases of one day together: 316 days) per case over 3 bars, -0.015 of the coin's usual move (8.38 %); normal drift in its direction -0.19 %, total -0.26 %; 617 cases
- Effect check (common/verdicts.md): no effect: t in the idea's direction -0.143 (below 1), 247 cases (30 needed)
Plan: `steps_cards/03_test_plan/night10_fallagishort_run/plans/047-02_falling-agitated-scaled-rise-fade_1d.md`
Record: `steps_cards/04_backtest/night10_fallagishort_run/backtests/047-02_falling-agitated-scaled-rise-fade_1d`
Measure: `measure.py`
