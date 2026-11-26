---
plan: 040-02_falling-calm-range-scaled-continuation_1d
idea: 040-02_falling-calm-range-scaled-continuation
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 3-bar move after short signals, short direction (day-clustered t): 0.00638197; t of the mean, cases summed per day: 1.58507 (threshold: confirm if t >= 2 (with supporting difference > 0); reject if t <= -2)
- Supporting check: top minus bottom half by |forecast| of mean unusual move (Welch t): 0.00449445, passed: True
- Counts: distinct case days: 434, cases: 715, top half cases: 357, bottom half cases: 358
- Decided by: With at least 30 case days, the numbers meet neither the confirm rule nor the reject rule.
- Reading: Profile taken as bars with regime 'unknown' (the detector's non-vetoed falling calm state) and the fall as a negative raw scaled_fall value; signals are forecast.md-7 bets (short size rising >= 2 points above its lowest level since the last bet, starting from 0 at each window start), the first bet of each 3-bar grid cell from the window's first row; drift is the mean of each coin's non-overlapping 3-bar grid returns pooled over all its windows; the t clusters case deviations summed per UTC day with a D/(D-1) correction; the median split puts |forecast| above the median in the top half and the rest in the bottom half; the plan's 30-day minimum is applied as 'not observable'.
- Size: unusual move +0.64 % (t 1.59, the cases of one day together: 434 days) per case over 3 bars, 0.072 of the coin's usual move (7.96 %); normal drift in its direction -0.39 %, total +0.25 %; 715 cases
Plan: `steps_cards/03_test_plan/night7_panic_run/plans/040-02_falling-calm-range-scaled-continuation_1d.md`
Record: `steps_cards/04_backtest/night7_panic_run/backtests/040-02_falling-calm-range-scaled-continuation_1d`
Measure: `measure.py`
