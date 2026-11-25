---
plan: 032-02.b2.g2.d1_near-low-rebound-in-falling-months_1d
idea: 032-02.b2.g2.d1_near-low-rebound-in-falling-months
fit: exact
status: inconclusive
---
Situation check: 98 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of (forecast/10) x excess next-day return on mean_reversion bars: 0.00261611; t of the mean, clustered by day: 1.29961 (threshold: confirm t >= 2 (with top-minus-bottom > 0); reject t <= -2)
- Supporting check: top third minus bottom third mean excess next-day return: 0.0119227, passed: True
- Counts: regime days with a position: 3174, regime bars in main measure: 3187, independent days (t clusters): 1188
- Decided by: main measure t between -2 and 2
- Reading: Situation recomputed per window from prices with bar range (high-low)/close, the 90/30 mean-range ratio and the 30-day return (the recorded fall30 raw value where present), falling back on the recorded regime where 90 bars of history are not in the record; the main measure uses every mean_reversion bar with a next-day return (zero forecasts included), its t clusters deviations by UTC day across coins; 'regime days with a position' are mean_reversion (coin, day) bars with a non-zero postRebalance_current_allocation; terciles are the lowest and highest n//3 regime bars pooled by forecast (stable sort).
- Size: unusual move +0.40 % (t 1.60, the cases of one day together: 678 days) per case over 1 bars, 0.089 of the coin's usual move (4.78 %); normal drift in its direction +0.12 %, total +0.52 %; 1363 cases
Plan: `steps_cards/03_test_plan/night7c_panic_run/plans/032-02.b2.g2.d1_near-low-rebound-in-falling-months_1d.md`
Record: `steps_cards/04_backtest/night7c_panic_run/backtests/032-02.b2.g2.d1_near-low-rebound-in-falling-months_1d`
Measure: `measure.py`
