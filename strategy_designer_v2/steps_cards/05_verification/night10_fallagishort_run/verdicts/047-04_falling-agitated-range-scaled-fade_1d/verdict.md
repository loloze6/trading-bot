---
plan: 047-04_falling-agitated-range-scaled-fade_1d
idea: 047-04_falling-agitated-range-scaled-fade
fit: exact
status: no effect
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 3-day fall after new short bets vs coin's falling-agitated grid mean: -0.00218047; t of the mean, cases of one day pooled: -0.441303 (threshold: above 0 with t >= 2 to confirm; below 0 with t <= -2 to reject; at least 30 case-days)
- Supporting check: unusual move of upper |forecast| half minus lower half: 0.0144519, passed: True
- Counts: case-days: 325, cases: 652
- Decided by: t between -2 and 2 (neither confirm nor reject rule met) No effect (common/verdicts.md): t in the idea's direction -0.441 (below 1), 325 cases (30 needed).
- Reading: the profile is regime 'unknown'; a case is the first new short bet (short forecast magnitude rising >= 2 from its lowest since the last bet) in each 3-bar grid cell from each window's first row, with a 3-bar return inside the window; the baseline pools each coin's profile grid bars over all its windows; the day-pooled t uses a clustered standard error with G/(G-1) correction; the median split puts |forecast| above the median in the upper half and the rest in the lower; fewer than 30 case-days is reported as not observable
- Size: unusual move -0.12 % (t -0.24, the cases of one day together: 325 days) per case over 3 bars, -0.020 of the coin's usual move (8.38 %); normal drift in its direction -0.19 %, total -0.31 %; 652 cases
- Effect check (common/verdicts.md): no effect: t in the idea's direction -0.441 (below 1), 325 cases (30 needed)
Plan: `steps_cards/03_test_plan/night10_fallagishort_run/plans/047-04_falling-agitated-range-scaled-fade_1d.md`
Record: `steps_cards/04_backtest/night10_fallagishort_run/backtests/047-04_falling-agitated-range-scaled-fade_1d`
Measure: `measure.py`
