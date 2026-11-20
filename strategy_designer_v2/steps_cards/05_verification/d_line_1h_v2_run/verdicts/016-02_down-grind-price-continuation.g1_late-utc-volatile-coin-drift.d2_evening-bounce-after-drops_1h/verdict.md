---
plan: 016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift.d2_evening-bounce-after-drops_1h
idea: 016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift.d2_evening-bounce-after-drops
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: forecast-weighted mean excess 2-bar return at forecast > 0 bars: 0.00135426; t of the weighted mean: 6.23541 (threshold: confirm: weighted mean > 0 with t >= 2 and upper-minus-lower half difference > 0; reject: weighted mean < 0 with t <= -2; min 300 cases)
- Supporting check: upper-half minus lower-half mean excess return (Welch t > 0): 0.000589731, passed: True
- Counts: cases with forecast > 0: 8613, upper half cases: 4306, lower half cases: 4306
- Decided by: The weighted mean excess return is positive with t >= 2 and the upper-minus-lower half difference is positive.
- Reading: Situation bars are those whose timestamp + 1h has hour 21 with a negative raw 'fall' value (24-bar return from prices where unrecorded); the t of the weighted mean is the ordinary t of the mean of forecast/mean(forecast) x excess return; the halves split the pooled cases sorted by forecast into the bottom floor(n/2) and top floor(n/2), the middle case dropped when n is odd; cases are forecast > 0 bars with a 2-bar return inside the window.
Plan: `steps_cards/03_test_plan/d_line_1h_v2_run/plans/016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift.d2_evening-bounce-after-drops_1h.md`
Record: `steps_cards/04_backtest/d_line_1h_v2_run/backtests/016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift.d2_evening-bounce-after-drops_1h`
Measure: `measure.py`
