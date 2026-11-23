---
plan: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d2_sunday-move-reverses-on-monday_1h
idea: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d2_sunday-move-reverses-on-monday
fit: exact
status: confirmed
---
Situation check: 99 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean signed 24-bar return of Monday 00:00 cases minus coin's mean non-overlapping 24-bar return, before costs: 0.00436512; t of the mean: 3.68175 (threshold: confirm: positive with t >= 2 and positive check; reject: negative with t <= -2; else inconclusive; at least 100 cases)
- Supporting check: mean signed excess return above minus below each coin's median 720-bar volatility: 0.00441706, passed: True
- Counts: cases with a position: 2081, cases above volatility median: 777, cases below volatility median: 777
- Decided by: The main measure is positive with t >= 2 and the supporting check is positive.
- Reading: The Monday 00:00 bar is the bar whose start timestamp + 1h is Monday 00:00 UTC; the Sunday move's sign is the recorded raw component (24-bar return from closes when missing); a case needs a non-zero position and forecast on that bar, the 24 bars are counted in rows of the same window, cases are pooled over coins, the volatility needs a full 720 hourly returns inside the window, and cases exactly at a coin's median are in neither group.
- Size: unusual move +0.44 % per case over 24 bars, 0.090 of the coin's usual move (4.87 %); normal drift in its direction -0.00 %, total +0.44 %; 2040 cases
Plan: `steps_cards/03_test_plan/retest_weekend_run/plans/026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d2_sunday-move-reverses-on-monday_1h.md`
Record: `steps_cards/04_backtest/retest_weekend_run/backtests/026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d2_sunday-move-reverses-on-monday_1h`
Measure: `measure.py`
