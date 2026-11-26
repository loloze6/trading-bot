---
plan: 074-01.g1_falling-agitated-wide-up-fade_1d
idea: 074-01.g1_falling-agitated-wide-up-fade
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual next-day move, short direction: 0.0135578; t of the mean, cases of one day pooled: 3.12198 (threshold: mean > 0 with t >= 2 to confirm; mean < 0 with t <= -2 to reject)
- Supporting check: wider half minus narrower half mean unusual move (|forecast| median split): 0.00641101, passed: True
- Counts: cases: 318, days: 210, wider half cases: 159, narrower half cases: 159
- Decided by: Mean unusual move above 0 with t >= 2 and the wider half beats the narrower half: confirm rule met.
- Reading: Situation computed from close-to-close return > 0 and the recorded width multiple (or high-low range over its 20-bar mean incl. the bar, recomputed when unrecorded) > 1.0, bars where it cannot be computed left out; a case is a bar with forecast < 0 whose previous bar in the window is not < 0 (a window's first bar counts if < 0); the wider half is |forecast| strictly above the cases' median, the narrower at or below; the plan's 'fewer than 100 cases' is applied as the minimum count (not observable).
- Size: unusual move +1.34 % (t 3.07, the cases of one day together: 214 days) per case over 1 bars, 0.295 of the coin's usual move (4.73 %); normal drift in its direction -0.13 %, total +1.21 %; 329 cases
- Direction check on folds A, D (the years step 7 does not explore): not judged: too few cases on the check folds (87 cases, 121 days)
Plan: `steps_cards/03_test_plan/night9_chopdeep_run/plans/074-01.g1_falling-agitated-wide-up-fade_1d.md`
Record: `steps_cards/04_backtest/night9_chopdeep_run/backtests/074-01.g1_falling-agitated-wide-up-fade_1d`
Measure: `measure.py`
