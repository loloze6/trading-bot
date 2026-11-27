---
plan: 061-01.b1.b1.b1.d1.d2.d2.d1_high-close-fall-falling-market_1d
idea: 061-01.b1.b1.b1.d1.d2.d2.d1_high-close-fall-falling-market
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-direction unusual 5-bar move over cases: 0.00669172; t of the mean, cases of one day summed: 1.00308 (threshold: confirm: mean > 0 with t >= 2 and slope > 0; reject: mean < 0 with t <= -2)
- Supporting check: OLS slope of unusual move on |forecast|: 0.00108141, passed: True
- Counts: cases: 1055, distinct days with cases: 390
- Decided by: t lies between -2 and 2, which the plan calls inconclusive.
- Reading: The 5-day return is the recorded fall5 raw value where present (else recomputed from closes), the falling profile is the 60-bar return below -10 % recomputed inside each window, and active bars whose 60-bar return cannot be computed (first 60 bars of a window) are left out of the agreement; a case is the first short bet (rise of the short forecast by >= 2 points from its low since the last bet) in each 5-bar grid cell counted from the window's first row, cases whose 5-bar return leaves the window are dropped, the day-clustered t uses the G/(G-1) correction, and fewer than 30 distinct case days gives 'not observable'.
- Size: unusual move +0.67 % (t 1.00, the cases of one day together: 390 days) per case over 5 bars, 0.054 of the coin's usual move (12.35 %); normal drift in its direction -0.82 %, total -0.15 %; 1055 cases
Plan: `steps_cards/03_test_plan/night9_chopagishort_run/plans/061-01.b1.b1.b1.d1.d2.d2.d1_high-close-fall-falling-market_1d.md`
Record: `steps_cards/04_backtest/night9_chopagishort_run/backtests/061-01.b1.b1.b1.d1.d2.d2.d1_high-close-fall-falling-market_1d`
Measure: `measure.py`
