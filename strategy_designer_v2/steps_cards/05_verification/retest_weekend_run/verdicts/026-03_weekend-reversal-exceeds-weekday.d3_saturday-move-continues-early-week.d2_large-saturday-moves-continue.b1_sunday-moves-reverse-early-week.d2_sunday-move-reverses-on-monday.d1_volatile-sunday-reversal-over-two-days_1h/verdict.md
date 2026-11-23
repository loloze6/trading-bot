---
plan: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d2_sunday-move-reverses-on-monday.d1_volatile-sunday-reversal-over-two-days_1h
idea: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d2_sunday-move-reverses-on-monday.d1_volatile-sunday-reversal-over-two-days
fit: exact
status: confirmed
---
Situation check: 99 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope of excess 48-bar return (%) on forecast: 0.0386618; t of slope: 2.60575 (threshold: confirm: positive with t >= 2; reject: negative with t <= -2)
- Supporting check: top-third minus bottom-third volatility slope, Welch t: 0.116271, passed: True
- Counts: cases across all coins: 2427, cases in top volatility third: 603, cases in bottom volatility third: 603
- Decided by: Confirm rule: the main slope is positive with t >= 2 and the volatility slope difference is positive with t >= 2.
- Reading: Situation = bar starting Sunday 23:00 UTC with forecast sign opposite to the raw scaled Sunday move; drift = coin's mean of non-overlapping 48-bar returns on each window's grid; volatility = std of the 720 one-bar returns ending at the entry close (cases with fewer bars in the window left out of the split); thirds = lowest and highest floor(n/3) cases per coin by volatility, pooled across coins; slopes by OLS with intercept, difference t = diff / sqrt(se_top^2 + se_bottom^2); too few cases gives 'not observable'.
- Size: unusual move +0.62 % per case over 48 bars, 0.097 of the coin's usual move (6.56 %); normal drift in its direction -0.00 %, total +0.62 %; 2021 cases
Plan: `steps_cards/03_test_plan/retest_weekend_run/plans/026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d2_sunday-move-reverses-on-monday.d1_volatile-sunday-reversal-over-two-days_1h.md`
Record: `steps_cards/04_backtest/retest_weekend_run/backtests/026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d2_sunday-move-reverses-on-monday.d1_volatile-sunday-reversal-over-two-days_1h`
Measure: `measure.py`
