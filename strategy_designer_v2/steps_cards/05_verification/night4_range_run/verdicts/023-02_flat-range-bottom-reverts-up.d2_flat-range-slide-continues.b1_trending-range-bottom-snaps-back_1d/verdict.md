---
plan: 023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues.b1_trending-range-bottom-snaps-back_1d
idea: 023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues.b1_trending-range-bottom-snaps-back
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled slope of 5-bar excess return on forecast, cells with forecast > 0: 0.00280011; OLS slope t: 3.78707 (threshold: confirm if slope t >= 2 (with mean excess > 0), reject if slope t <= -2)
- Supporting check: mean excess 5-bar return over those cells: 0.000847719, passed: True
- Counts: grid cells with a forecast above 0, pooled over coins: 565
- Decided by: The slope's t is 2 or more and the mean excess return is above 0.
- Reading: Net move to range taken as |close[t]-close[t-30]| over the 30-bar high-low range, the Ichimoku position as close minus the 30-bar high-low midpoint, the 10-day fall from fall10's raw value (else recomputed from closes), active bars whose 30-bar history is not inside the window left out of the agreement; the coin's mean 5-bar return is the mean over all grid cells of all its windows, and the slope t is the OLS slope t of the pooled regression of excess return on forecast.
- Size: unusual move -0.37 % per case over 5 bars, -0.030 of the coin's usual move (10.60 %); normal drift in its direction +0.60 %, total +0.23 %; 751 cases
Plan: `steps_cards/03_test_plan/night4_range_run/plans/023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues.b1_trending-range-bottom-snaps-back_1d.md`
Record: `steps_cards/04_backtest/night4_range_run/backtests/023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues.b1_trending-range-bottom-snaps-back_1d`
Measure: `measure.py`
