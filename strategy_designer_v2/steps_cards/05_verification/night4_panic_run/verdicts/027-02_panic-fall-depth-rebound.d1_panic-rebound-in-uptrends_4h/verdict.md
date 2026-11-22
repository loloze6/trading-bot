---
plan: 027-02_panic-fall-depth-rebound.d1_panic-rebound-in-uptrends_4h
idea: 027-02_panic-fall-depth-rebound.d1_panic-rebound-in-uptrends
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 84-bar return of long bets (one per 84-bar grid cell): 0.0441516; t of the mean: 1.25769 (threshold: confirm: mean > 0 with t >= 2 over >= 30 cases (and supporting check passes); reject: mean < 0 with t <= -2 over >= 30 cases)
- Supporting check: mean unusual return, forecast above cases' median minus at or below: None, passed: False
- Counts: cases: 90, cases above median: 0, cases at or below median: 90, active bars: 403
- Decided by: t between -2 and 2 over at least 30 cases
- Reading: A case is the first long bet (forecast rise >= 2 from its lowest positive level since the last bet, from 0 after flat) in each 84-bar grid cell counted from each window's first row, with a full 84-bar return inside the window; drift is each coin's mean non-overlapping 84-bar return over all its windows; panic taken from the recorded regime or the recomputed high-low range ratio.
- Size: unusual move +4.42 % per case over 84 bars, 0.196 of the coin's usual move (17.66 %); normal drift in its direction +2.37 %, total +6.78 %; 90 cases
Plan: `steps_cards/03_test_plan/night4_panic_run/plans/027-02_panic-fall-depth-rebound.d1_panic-rebound-in-uptrends_4h.md`
Record: `steps_cards/04_backtest/night4_panic_run/backtests/027-02_panic-fall-depth-rebound.d1_panic-rebound-in-uptrends_4h`
Measure: `measure.py`
