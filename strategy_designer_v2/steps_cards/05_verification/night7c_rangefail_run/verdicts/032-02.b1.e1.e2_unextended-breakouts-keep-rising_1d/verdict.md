---
plan: 032-02.b1.e1.e2_unextended-breakouts-keep-rising_1d
idea: 032-02.b1.e1.e2_unextended-breakouts-keep-rising
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: Welch t of 20-bar excess return, forecast above vs at/below cases' median: -0.0259629; Welch t: -0.531936 (threshold: confirm: t >= 2 with forecast-weighted mean excess > 0; reject: t <= -2)
- Supporting check: forecast-weighted mean 20-bar excess return of cases: -0.0167928, passed: False
- Counts: non-overlapping break cases: 205, cases above median forecast: 102, cases at or below median forecast: 103
- Decided by: The main t lies between -2 and 2 (inconclusive rule).
- Reading: Situation check uses only active bars with 60 prior closes inside the same window (149 active bars without them left out); cases are pooled over all coins and windows, a break is counted only if it is at least 20 bars after the last counted one in its coin-window, the forecast median is taken over all pooled cases, the coin's mean 20-bar return is from the 0,20,40,... grid of each window pooled over its windows, and minimum counts not reached give 'not observable'.
- Size: unusual move -1.83 % (t -0.60, the cases of one day together: 69 days) per case over 20 bars, -0.034 of the coin's usual move (21.24 %); normal drift in its direction +2.66 %, total +0.83 %; 88 cases
Plan: `steps_cards/03_test_plan/night7c_rangefail_run/plans/032-02.b1.e1.e2_unextended-breakouts-keep-rising_1d.md`
Record: `steps_cards/04_backtest/night7c_rangefail_run/backtests/032-02.b1.e1.e2_unextended-breakouts-keep-rising_1d`
Measure: `measure.py`
