---
plan: 021-02_below-falling-cloud-continues-down_1d
idea: 021-02_below-falling-cloud-continues-down
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-signed 26-bar excess return over the coin's mean, on grid bars with forecast < 0: 0.015116; t of the mean: 0.689244 (threshold: confirm: mean > 0 with t >= 2 over at least 30 cases; reject: mean < 0 with t <= -2 over at least 30 cases)
- Supporting check: OLS slope of short-signed excess return on |forecast|: -0.0091762, passed: False
- Counts: cases: 156
- Decided by: The t-statistic lies between -2 and 2, which the plan calls inconclusive.
- Reading: The cloud position is recomputed from each window's own prices (standard Ichimoku 9/26/52 with 26-bar displacement, close below the lower span), the slope is the recorded cloud_slope raw value (recomputed where missing), and active bars whose cloud cannot be computed inside their window are left out of the agreement share; cases are grid bars at positions 0, 26, 52, ... of each window with a full 26-bar return inside the window, and the coin's mean 26-bar return is taken over the same grid across all its windows.
- Size: unusual move +1.51 % per case over 26 bars, 0.071 of the coin's usual move (25.48 %); normal drift in its direction -4.24 %, total -2.73 %; 231 cases
Plan: `steps_cards/03_test_plan/night3_ichimoku_run/plans/021-02_below-falling-cloud-continues-down_1d.md`
Record: `steps_cards/04_backtest/night3_ichimoku_run/backtests/021-02_below-falling-cloud-continues-down_1d`
Measure: `measure.py`
