---
plan: 058-01_agitated-decline-rally-giveback_1d
idea: 058-01_agitated-decline-rally-giveback
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 5-day move in the short direction per short-bet case: 0.00332497; t of the mean, cases of one day pooled: 0.485258 (threshold: confirm: mean > 0 with t >= 2; reject: t <= -2)
- Supporting check: share given back, top minus bottom half of |forecast|, Welch t: -1.86817, passed: False
- Counts: cases: 422, distinct days: 244, top half cases: 203, bottom half cases: 202
- Decided by: Inconclusive: enough cases, but the numbers meet neither the confirm rule (both t >= 2) nor the reject rule (either t <= -2).
- Reading: A case is the first short bet (|forecast| rising >= 2 from its lowest size since the last bet, reset at flat or side change) in each 5-bar grid cell of a window, the share given back is the short-direction unusual move over the 3-day price rise to that bar, and the halves are split by sorting cases on |forecast| (ties by time) with the lower floor(n/2) as the bottom half.
- Size: unusual move +0.33 % (t 0.49, the cases of one day together: 244 days) per case over 5 bars, 0.025 of the coin's usual move (10.60 %); normal drift in its direction -0.65 %, total -0.32 %; 422 cases
Plan: `steps_cards/03_test_plan/night8_fallingagitated_run/plans/058-01_agitated-decline-rally-giveback_1d.md`
Record: `steps_cards/04_backtest/night8_fallingagitated_run/backtests/058-01_agitated-decline-rally-giveback_1d`
Measure: `measure.py`
