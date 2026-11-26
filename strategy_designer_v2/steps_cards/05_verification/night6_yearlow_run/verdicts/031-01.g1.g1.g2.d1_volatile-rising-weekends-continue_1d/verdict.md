---
plan: 031-01.g1.g1.g2.d1_volatile-rising-weekends-continue_1d
idea: 031-01.g1.g1.g2.d1_volatile-rising-weekends-continue
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 2-bar move (Fri close to Sun close) minus normal 2-day drift, per case: 0.0141234; t of the mean, cases clustered by day: 3.74925 (threshold: confirm: mean > 0 with t >= 2 and check passes; reject: mean < 0 with t <= -2)
- Supporting check: mean unusual move at/above median forecast minus below median: -0.000474163, passed: False
- Counts: days with cases: 207, cases: 508
- Decided by: t >= 2 but the supporting check failed: inconclusive per the plan.
- Reading: Friday close = a bar whose UTC start time is a Friday (next bar Saturday); the volatility ratio is recomputed in each window as the 20-day over the 60-day std (ddof 1) of daily close returns and the agreement is taken over the active bars where it is computable (Friday, rise and side only if none is); the 14-day rise sign is read from rise_vol's raw value (positive ratio) or the 14-day price return; cases are long forecast rises of at least 2 points, once per 2-bar grid cell, with the 2-bar return inside the window, the drift is the mean non-overlapping 2-bar return over all the coin's windows, the t clusters cases by UTC day, the median split uses the forecast at the case bar, and the plan's 'at least 30 days with cases' minimum gives 'not observable' when not reached.
- Size: unusual move +1.41 % (t 3.76, the cases of one day together: 207 days) per case over 2 bars, 0.205 of the coin's usual move (6.58 %); normal drift in its direction +0.24 %, total +1.65 %; 508 cases
Plan: `steps_cards/03_test_plan/night6_yearlow_run/plans/031-01.g1.g1.g2.d1_volatile-rising-weekends-continue_1d.md`
Record: `steps_cards/04_backtest/night6_yearlow_run/backtests/031-01.g1.g1.g2.d1_volatile-rising-weekends-continue_1d`
Measure: `measure.py`
