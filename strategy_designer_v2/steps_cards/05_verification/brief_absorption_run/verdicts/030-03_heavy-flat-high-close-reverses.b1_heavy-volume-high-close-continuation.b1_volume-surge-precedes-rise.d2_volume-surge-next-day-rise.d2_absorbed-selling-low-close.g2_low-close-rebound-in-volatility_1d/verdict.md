---
plan: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.g2_low-close-rebound-in-volatility_1d
idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.g2_low-close-rebound-in-volatility
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of excess next-day return on post_pipeline_value, pooled: 0.000344049; OLS slope t: 5.64463 (threshold: slope t >= 2 confirms (with the check), slope t <= -2 rejects)
- Supporting check: lower-half closes: mean excess return high-vol minus low-vol (Welch t >= 2): 0.00380959, passed: True
- Counts: bars in the regression: 17380, high-volatility group: 4015, low-volatility group: 4052
- Decided by: Confirm: the slope's t is 2 or more and the supporting check's Welch t is 2 or more.
- Reading: Every bar with a next-day return inside its window is pooled (h=1, so no overlap); the coin's mean is its mean next-day return over all windows; 'lower half' is (high-close)/(high-low) > 0.5; the 20-day volatility is the component's own (raw / location, else the ddof-1 std of the last 20 daily returns within the window), split at the coin's median over all its bars (above = top half); the plan's 'inconclusive' for too few cases is reported as 'not observable' as the workflow requires.
- Size: unusual move +0.14 % per case over 1 bars, 0.030 of the coin's usual move (4.78 %); normal drift in its direction +0.12 %, total +0.26 %; 6917 cases
Plan: `steps_cards/03_test_plan/brief_absorption_run/plans/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.g2_low-close-rebound-in-volatility_1d.md`
Record: `steps_cards/04_backtest/brief_absorption_run/backtests/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.g2_low-close-rebound-in-volatility_1d`
Measure: `measure.py`
