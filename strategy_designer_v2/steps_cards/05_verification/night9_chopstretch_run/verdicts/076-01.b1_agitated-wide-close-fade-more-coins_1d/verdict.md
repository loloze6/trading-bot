---
plan: 076-01.b1_agitated-wide-close-fade-more-coins_1d
idea: 076-01.b1_agitated-wide-close-fade-more-coins
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-side unusual next-bar move on forecast<0 bars: -0.0054794; t of the mean, cases of one day together: -1.84897 (threshold: confirm: mean > 0 with day-clustered t >= 2 and supporting check passes; reject: t <= -2)
- Supporting check: mean move of larger |forecast| half minus smaller half: 0.00979641, passed: True
- Counts: distinct days with a case: 866, cases: 2138
- Decided by: t between -2 and 2.
- Reading: Agitated profile read from the recorded regime; cases are every forecast<0 bar with a next close in its window (1-bar grid, no overlap); the day-clustered t sums deviations per UTC day with a small-sample factor d/(d-1); the larger half is |forecast| strictly above the median, the smaller half at or below it.
- Size: unusual move -0.35 % (t -1.05, the cases of one day together: 714 days) per case over 1 bars, -0.066 of the coin's usual move (5.33 %); normal drift in its direction -0.13 %, total -0.49 %; 1613 cases
Plan: `steps_cards/03_test_plan/night9_chopstretch_run/plans/076-01.b1_agitated-wide-close-fade-more-coins_1d.md`
Record: `steps_cards/04_backtest/night9_chopstretch_run/backtests/076-01.b1_agitated-wide-close-fade-more-coins_1d`
Measure: `measure.py`
