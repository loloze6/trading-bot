---
plan: 054-02_strong-close-reclaim-rebound_1d
idea: 054-02_strong-close-reclaim-rebound
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess 5-bar return of cases over the coin's falling-agitated 5-bar mean: 0.0105699; t of the mean, cases of one day taken together: 0.620149 (threshold: confirm: mean > 0 with t >= 2 (and upper half beats lower half); reject: mean < 0 with t <= -2; at least 30 cases)
- Supporting check: upper-half minus lower-half mean excess return (median forecast split): None, passed: False
- Counts: cases: 76, days: 49
- Decided by: The t of the mean excess return lies between -2 and 2.
- Reading: Falling agitated bars are taken as bars whose regime is not 'chop' (the profile vetoes set chop), the pierce is rebuilt from the reclaim raw value (low30 = close - value x range, low < low30 <= close) or from prices when not recorded, a case is the first long bet (forecast rise >= 2 from its lowest level since the last bet, from 0 after a flat) in each 5-bar grid cell of a window, the day-clustered t uses deviations summed per day with a D/(D-1) correction, and the median split puts forecasts above the median in the upper half and the rest in the lower half.
- Size: unusual move +1.29 % (t 0.76, the cases of one day together: 49 days) per case over 5 bars, 0.119 of the coin's usual move (10.60 %); normal drift in its direction +0.64 %, total +1.93 %; 76 cases
Plan: `steps_cards/03_test_plan/pilot_panic_run/plans/054-02_strong-close-reclaim-rebound_1d.md`
Record: `steps_cards/04_backtest/pilot_panic_run/backtests/054-02_strong-close-reclaim-rebound_1d`
Measure: `measure.py`
