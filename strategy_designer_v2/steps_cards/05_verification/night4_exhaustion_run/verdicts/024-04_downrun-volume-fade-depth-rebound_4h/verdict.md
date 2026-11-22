---
plan: 024-04_downrun-volume-fade-depth-rebound_4h
idea: 024-04_downrun-volume-fade-depth-rebound
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 18-bar excess return of long bets over the coin's normal 18-bar drift: 0.000601472; ordinary t of the mean: 0.541391 (threshold: confirm: mean > 0 with t >= 2 over >= 30 cases; reject: mean < 0 with t <= -2 over >= 30 cases)
- Supporting check: mean excess return above-median minus below-median raw volume_fade: -0.00582804, passed: False
- Counts: cases: 5713, above_median_cases: 1120, below_median_cases: 1077, active_bars: 51676
- Decided by: The t lies between -2 and 2 (or is undefined), meeting neither the confirm nor the reject rule.
- Reading: Situation = bar closing below the previous close with a positive forecast; a case is the first long bet (forecast rise >= 2 from its lowest positive level since the last bet, reset at 0) in each 18-bar cell counted from each window's first row, with its 18-bar return inside the window; drift = mean of the coin's non-overlapping 18-bar returns over all windows; the median split puts cases strictly above vs strictly below the median and drops ties; fewer than 30 cases is reported as not observable per the workflow.
- Size: unusual move +0.06 % per case over 18 bars, 0.008 of the coin's usual move (8.17 %); normal drift in its direction +0.41 %, total +0.47 %; 5713 cases
Plan: `steps_cards/03_test_plan/night4_exhaustion_run/plans/024-04_downrun-volume-fade-depth-rebound_4h.md`
Record: `steps_cards/04_backtest/night4_exhaustion_run/backtests/024-04_downrun-volume-fade-depth-rebound_4h`
Measure: `measure.py`
