---
plan: 061-01.b1.b1.b1.d1.d1.d1.d1_choppy-deep-month-fall-continues_1d
idea: 061-01.b1.b1.b1.d1.d1.d1.d1_choppy-deep-month-fall-continues
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual move of short cases over 5 bars (short side positive): 0.0124242; t of the mean, cases of one day taken together: 2.24679 (threshold: t of 2 or more (with supporting check above 0) confirms; t of -2 or less rejects; at least 30 distinct days of cases)
- Supporting check: mean unusual move of larger-short half minus smaller-short half: -0.0091532, passed: False
- Counts: cases: 676, distinct days of cases: 432
- Decided by: A confirm-level t with the supporting check at or below 0 is inconclusive.
- Reading: Situation bars: 20-day return (recorded fall20 raw value, else from closes) at or below -10 and 60-day return from closes between -10 and +10 inclusive, short side; active bars in a window's first 60 rows, where the 60-day return cannot be computed inside the window, are left out of the agreement; a case is a short bet (forecast rising on the short side by at least 2 points from its lowest level since the last bet), the first one in each 5-bar grid cell of its window, its return from that bar's close over 5 bars; position size is the absolute postRebalance_current_allocation on the case bar, the larger-short half being the top floor(n/2) cases by size; the day-clustered t uses a G/(G-1) correction.
- Size: unusual move +1.24 % (t 2.25, the cases of one day together: 432 days) per case over 5 bars, 0.089 of the coin's usual move (12.35 %); normal drift in its direction -0.82 %, total +0.42 %; 676 cases
Plan: `steps_cards/03_test_plan/night9_chopagishort_run/plans/061-01.b1.b1.b1.d1.d1.d1.d1_choppy-deep-month-fall-continues_1d.md`
Record: `steps_cards/04_backtest/night9_chopagishort_run/backtests/061-01.b1.b1.b1.d1.d1.d1.d1_choppy-deep-month-fall-continues_1d`
Measure: `measure.py`
