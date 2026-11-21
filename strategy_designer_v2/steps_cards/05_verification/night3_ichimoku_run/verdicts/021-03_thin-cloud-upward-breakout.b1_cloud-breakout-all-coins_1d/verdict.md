---
plan: 021-03_thin-cloud-upward-breakout.b1_cloud-breakout-all-coins_1d
idea: 021-03_thin-cloud-upward-breakout.b1_cloud-breakout-all-coins
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: thin minus thick cloud unusual 26-bar return: 0.0707546; Welch t: 1.59277 (threshold: difference > 0 with Welch t >= 2 to confirm; Welch t <= -2 to reject)
- Supporting check: all-case mean unusual 26-bar return > 0 with t >= 2: 0.0222315, passed: False
- Counts: cases: 285, thin_cases: 142, thick_cases: 143
- Decided by: Neither the confirm rule (difference > 0, Welch t >= 2, with supporting check passed) nor the reject rule (t <= -2) is met.
- Reading: agreement measured on active bars where the cloud (9/26/52, displacement 26) and the cross origin are computable from the window's prices; a case is a bar where the forecast rises by at least 2 from 0 on the previous bar, the first such in each 26-bar grid cell from the window's first row, thin cases have raw proximity strictly above the median of all cases and the rest are thick, and the plan's 'inconclusive with few cases' is reported as not observable.
- Size: unusual move +2.32 % per case over 26 bars, 0.081 of the coin's usual move (30.33 %); normal drift in its direction +5.58 %, total +7.91 %; 359 cases
Plan: `steps_cards/03_test_plan/night3_ichimoku_run/plans/021-03_thin-cloud-upward-breakout.b1_cloud-breakout-all-coins_1d.md`
Record: `steps_cards/04_backtest/night3_ichimoku_run/backtests/021-03_thin-cloud-upward-breakout.b1_cloud-breakout-all-coins_1d`
Measure: `measure.py`
