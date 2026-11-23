---
plan: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d2_sunday-move-reverses-on-monday.d3_moderate-sunday-moves-reverse-most_1h
idea: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d2_sunday-move-reverses-on-monday.d3_moderate-sunday-moves-reverse-most
fit: exact
status: confirmed
---
Situation check: 99 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of the slope of 48-bar excess return on the forecast, pooled: 3.41073; OLS slope t: 3.41073 (threshold: confirm if t >= +2 and mean signed unusual move > 0; reject if t <= -2; inconclusive otherwise)
- Supporting check: mean signed unusual move over the cases, before costs: 0.0056026, passed: True
- Counts: cases in total: 2414, cases BTCUSD: 409, cases ETHUSD: 410, cases LTCUSD: 409, cases XMRUSD: 403, cases XRPUSD: 410, cases ZECUSD: 373
- Decided by: The slope's t is +2 or more and the mean signed unusual move is above 0.
- Reading: Sunday's last bar is the bar starting Sunday 23:00 UTC (its close ends Sunday); Sunday's move is the sign of the component's raw value (24-bar price return where it is missing); a case is such a bar with a nonzero forecast and a 48-bar forward return inside its window; the normal drift is the coin's mean 48-bar return on the non-overlapping grid of all its windows; the slope t is the ordinary OLS t.
- Size: unusual move +0.63 % per case over 48 bars, 0.096 of the coin's usual move (6.56 %); normal drift in its direction -0.01 %, total +0.62 %; 2080 cases
Plan: `steps_cards/03_test_plan/retest_weekend_run/plans/026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d2_sunday-move-reverses-on-monday.d3_moderate-sunday-moves-reverse-most_1h.md`
Record: `steps_cards/04_backtest/retest_weekend_run/backtests/026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d2_sunday-move-reverses-on-monday.d3_moderate-sunday-moves-reverse-most_1h`
Measure: `measure.py`
