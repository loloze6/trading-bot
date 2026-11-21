---
plan: 020-02_support-retest-bounces-up_1d
idea: 020-02_support-retest-bounces-up
fit: adapted
status: rejected
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: forecast-weighted mean 5-bar excess return of cases: -0.00555971; t of the forecast-weighted mean: -2.10274 (threshold: confirm: mean > 0 with t >= 2 and Spearman > 0; reject: t <= -2)
- Supporting check: Spearman(forecast, 5-bar excess return): -0.0174067, passed: False
- Counts: independent cases: 1401
- Decided by: The forecast-weighted mean excess return has t <= -2.
- Reading: Situation = close below its close 5 bars earlier in the same window and the raw swing-low nearness count > 0, side long, with active bars lacking the 5-bar-earlier close or the raw value left out; a case is the first long bet (forecast rise >= 2 points from its lowest level since the last bet, from 0 after flat) in each 5-bar grid cell of a window, weighted by its forecast, the drift is the coin's mean 5-bar return on the grid of all its windows, and the t of the weighted mean uses the weighted (sandwich) standard error with n/(n-1) correction.
- Size: unusual move -0.57 % per case over 5 bars, -0.046 of the coin's usual move (10.60 %); normal drift in its direction +0.58 %, total +0.02 %; 1401 cases
Plan: `steps_cards/03_test_plan/night3_levels_run/plans/020-02_support-retest-bounces-up_1d.md`
Record: `steps_cards/04_backtest/night3_levels_run/backtests/020-02_support-retest-bounces-up_1d`
Measure: `measure.py`
