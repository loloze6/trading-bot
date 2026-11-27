---
plan: 070-01.g1_calm-decline-long-run-break_1d
idea: 070-01.g1_calm-decline-long-run-break
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: abs(forecast)-weighted mean short-side next-day excess move: 0.00628636; t of the weighted mean, clustered by day: 2.38868 (threshold: confirm: > 0 with t >= 2 over >= 30 case-days; reject: < 0 with t <= -2 over >= 30 case-days)
- Supporting check: mean next-day excess return, breaks of 2+ down days minus breaks of 1: -0.00917353, passed: True
- Counts: case-days: 286, cases: 465, breaks of 2+ down days: 442, breaks of a single down day: 389
- Decided by: Main measure positive with t >= 2 over at least 30 case-days and the supporting difference below 0.
- Reading: Falling calm is taken as the detector's 'unknown' (not vetoed) regime on each bar, both for the situation check and for the supporting check's profile (the 60-bar trend and 365-bar vol percentile cannot be rebuilt inside a window), run lengths are rebuilt from window closes with single-day breaks kept only when the run's start is seen, the t clusters weighted deviations by calendar day with a G/(G-1) correction, and case-days are the distinct days with a short forecast.
- Size: unusual move +0.63 % (t 2.39, the cases of one day together: 286 days) per case over 1 bars, 0.134 of the coin's usual move (4.73 %); normal drift in its direction -0.13 %, total +0.50 %; 465 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.002493 on the check folds against +0.006286 on every fold
Plan: `steps_cards/03_test_plan/night9_fallcalmfade_run/plans/070-01.g1_calm-decline-long-run-break_1d.md`
Record: `steps_cards/04_backtest/night9_fallcalmfade_run/backtests/070-01.g1_calm-decline-long-run-break_1d`
Measure: `measure.py`
