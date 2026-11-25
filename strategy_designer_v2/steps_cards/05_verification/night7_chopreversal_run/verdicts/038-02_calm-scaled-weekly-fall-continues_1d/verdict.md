---
plan: 038-02_calm-scaled-weekly-fall-continues_1d
idea: 038-02_calm-scaled-weekly-fall-continues
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 5-bar move in the short direction, before costs: 0.00554501; t of the mean, cases of one day summed together: 1.53369 (threshold: confirm: mean > 0 with t >= 2 (and slope > 0); reject: mean < 0 with t <= -2)
- Supporting check: OLS slope of short-direction unusual 5-bar return on abs(forecast), grid bars with forecast < 0: 0.000394984, passed: True
- Counts: cases: 1093, distinct days: 616, supporting grid bars: 888
- Decided by: t between -2 and 2: inconclusive rule.
- Reading: A case is the first short bet (rise of abs(forecast) of at least 2 points from its lowest short level since the last bet) in each 5-bar grid cell of a window, measured from that bar's close over 5 bars, with drift the coin's mean non-overlapping 5-bar grid return over all windows; the situation is a negative raw scaled 7-bar return (price 7-bar return where the raw value is missing) on a short forecast, the calm profile being the code's regime gate.
- Size: unusual move +0.55 % (t 1.53, the cases of one day together: 616 days) per case over 5 bars, 0.058 of the coin's usual move (10.60 %); normal drift in its direction -0.65 %, total -0.09 %; 1093 cases
Plan: `steps_cards/03_test_plan/night7_chopreversal_run/plans/038-02_calm-scaled-weekly-fall-continues_1d.md`
Record: `steps_cards/04_backtest/night7_chopreversal_run/backtests/038-02_calm-scaled-weekly-fall-continues_1d`
Measure: `measure.py`
