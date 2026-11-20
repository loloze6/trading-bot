---
plan: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e2_short-drift-after-strong-highs.g1_range-low-weakness-above-trend_1d
idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e2_short-drift-after-strong-highs.g1_range-low-weakness-above-trend
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of (forecast/10) x excess 5-bar return on trending grid bars: 0.00438321; ordinary t of the mean: 2.84017 (threshold: t >= 2 confirms (with check < 0); t <= -2 rejects; otherwise inconclusive; needs >= 100 active grid cases and >= 30 with forecast < 0)
- Supporting check: mean excess 5-bar return, forecast < -10 minus forecast == 0 (active grid bars): -0.0242881, passed: True
- Counts: active grid cases: 1674, active grid cases with forecast below 0: 642, grid cases with forecast below -10: 279, grid cases with forecast 0: 1032
- Decided by: Main-measure t is 2 or more and the supporting check's difference is below 0.
- Reading: Active grid cases are taken as grid bars with regime == trending (the forecast is active only in that regime, so forecast-0 trending bars are the check's comparison group), the coin's mean 5-bar return is the mean of its non-overlapping grid returns over all windows and regimes, the situation is the range_pos raw value <= 0 in the trending regime on the short side, and a minimum-count shortfall is reported as not observable.
- Size: unusual move +1.01 % per case over 5 bars, 0.090 of the coin's usual move (10.60 %); normal drift in its direction -0.58 %, total +0.42 %; 750 cases
Plan: `steps_cards/03_test_plan/demo_run/plans/002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e2_short-drift-after-strong-highs.g1_range-low-weakness-above-trend_1d.md`
Record: `steps_cards/04_backtest/demo_run/backtests/002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e2_short-drift-after-strong-highs.g1_range-low-weakness-above-trend_1d`
Measure: `measure.py`
