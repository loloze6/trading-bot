---
plan: 031-03.g1.b1.d2.e1_rally-on-fading-volume-fails_1d
idea: 031-03.g1.b1.d2.e1_rally-on-fading-volume-fails
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-direction 14-bar unusual move (return minus drift, sign flipped): 0.000992725; t of the mean, clustered by day: 0.094139 (threshold: mean > 0 with day-clustered t >= 2 confirms; mean < 0 with t <= -2 rejects)
- Supporting check: correlation of signal-bar forecast with 14-bar excess return: 0.0107618, passed: True
- Counts: cases: 1225, distinct days: 645
- Decided by: t lies between -2 and 2, so the idea is neither confirmed nor rejected.
- Reading: Situation recomputed as close[t]/close[t-14]-1 > 0 and the recorded 'dry' raw volume ratio (recomputed 14/30 mean volume - 1 where not recorded) < 0, expected side short, with active bars whose 14-bar return cannot be computed inside the window left out of the agreement; a case is the first short bet (short forecast deepening by >= 2 points from its lowest short level since the last bet, reset at flat or side change) in each 14-bar grid cell of a window, counted only if its 14-bar forward return lies inside the window, drift is the coin's mean non-overlapping 14-bar return over all its windows, the day-clustered t uses a G/(G-1) correction, and fewer than 30 distinct days is reported as not observable.
- Size: unusual move +0.10 % (t 0.09, the cases of one day together: 645 days) per case over 14 bars, 0.018 of the coin's usual move (20.98 %); normal drift in its direction -2.47 %, total -2.38 %; 1225 cases
Plan: `steps_cards/03_test_plan/night6_longreversal_run/plans/031-03.g1.b1.d2.e1_rally-on-fading-volume-fails_1d.md`
Record: `steps_cards/04_backtest/night6_longreversal_run/backtests/031-03.g1.b1.d2.e1_rally-on-fading-volume-fails_1d`
Measure: `measure.py`
