---
plan: 061-01.b1.b1.b1.d2.d3.d2_pullback-high-close-fade_1d
idea: 061-01.b1.b1.b1.d2.d3.d2_pullback-high-close-fade
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-direction 5-bar excess return over drift per case: 0.0146226; t of the mean, cases of one day summed: 1.46789 (threshold: confirm: mean > 0 with t >= 2 over >= 30 cases (and supporting check); reject: t <= -2 over >= 30 cases)
- Supporting check: larger-half minus smaller-half mean excess (by forecast size): 0.0171608, passed: True
- Counts: cases: 90, distinct days: 81
- Decided by: The t lies between -2 and 2.
- Reading: A case is the first short bet (forecast deepening by >= 2 points from its shallowest short level since the last bet, reset at flat) in each 5-bar grid cell of a window with 5 bars ahead in that window; the minimum requires both 30 cases and 30 distinct days; the halves are by |forecast| on the case bar, the middle case dropped when the count is odd; the day-clustered t uses a G/(G-1) correction.
- Size: unusual move +1.46 % (t 1.48, the cases of one day together: 81 days) per case over 5 bars, 0.140 of the coin's usual move (11.68 %); normal drift in its direction -0.66 %, total +0.80 %; 90 cases
Plan: `steps_cards/03_test_plan/night9_chopagishort_run/plans/061-01.b1.b1.b1.d2.d3.d2_pullback-high-close-fade_1d.md`
Record: `steps_cards/04_backtest/night9_chopagishort_run/backtests/061-01.b1.b1.b1.d2.d3.d2_pullback-high-close-fade_1d`
Measure: `measure.py`
