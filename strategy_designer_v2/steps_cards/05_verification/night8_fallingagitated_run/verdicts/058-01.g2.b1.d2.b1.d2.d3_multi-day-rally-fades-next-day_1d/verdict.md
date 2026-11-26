---
plan: 058-01.g2.b1.d2.b1.d2.d3_multi-day-rally-fades-next-day_1d
idea: 058-01.g2.b1.d2.b1.d2.d3_multi-day-rally-fades-next-day
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-direction unusual next-day move: 0.0044517; t of the mean, cases pooled by day: 1.73619 (threshold: confirm if t >= 2 (and size check > 0); reject if t <= -2; else inconclusive)
- Supporting check: larger-half minus smaller-half mean unusual move (|forecast| median split): 0.00419551, passed: True
- Counts: distinct case days: 494, cases: 1291, larger half cases: 645, smaller half cases: 646
- Decided by: The t lies between -2 and 2, which the plan calls inconclusive.
- Reading: The falling-agitated profile and the up-day rule are taken from the recorded regime ('mean_reversion', since the detector's components are not recorded and their 60/365-day lookbacks exceed the window), plus the up day from prices and a positive raw rally, short side; cases are all bars with forecast below 0 with a next close in the window, the coin's mean daily return is over all its windows, t is clustered by UTC day, the larger half is |forecast| strictly above the median and the 30 distinct case days minimum is treated as the plan's minimum count.
- Size: unusual move +0.58 % (t 1.86, the cases of one day together: 386 days) per case over 1 bars, 0.112 of the coin's usual move (5.33 %); normal drift in its direction -0.14 %, total +0.44 %; 913 cases
Plan: `steps_cards/03_test_plan/night8_fallingagitated_run/plans/058-01.g2.b1.d2.b1.d2.d3_multi-day-rally-fades-next-day_1d.md`
Record: `steps_cards/04_backtest/night8_fallingagitated_run/backtests/058-01.g2.b1.d2.b1.d2.d3_multi-day-rally-fades-next-day_1d`
Measure: `measure.py`
