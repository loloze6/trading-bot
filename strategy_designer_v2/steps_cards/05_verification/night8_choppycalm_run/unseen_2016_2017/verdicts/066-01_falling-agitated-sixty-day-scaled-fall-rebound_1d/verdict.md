---
plan: 066-01_falling-agitated-sixty-day-scaled-fall-rebound_1d
idea: 066-01_falling-agitated-sixty-day-scaled-fall-rebound
fit: adapted
status: not observable
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: forecast-weighted mean next-day return minus coin's mean daily return: 0.00623995; t of weighted mean, same-day cases summed: 1.01621 (threshold: confirm: > 0 with t >= 2 and slope > 0; reject: t <= -2)
- Supporting check: OLS slope of excess next-day return on forecast: 0.00153777, passed: True
- Counts: cases: 19, distinct days: 19, active bars: 19
- Decided by: The plan's minimum of 100 cases on 50 distinct days is not reached (19 cases on 19 days).
- Reading: The falling agitated profile is read from the recorded regime (the only regime with a strategy, 'unknown', is the one where both profile vetoes passed). A falling day is a negative raw scaled return, or a negative close-to-close return when the raw value is missing. The coin's mean daily return is the mean of all its within-window close-to-close returns. The t of the weighted mean sums the cases' weighted deviations f*(x-m) per UTC day and uses SE = sqrt(D/(D-1) * sum of squared day sums) / sum(f). The plan's minimum counts are taken as 100 cases and 50 distinct days, and missing them gives 'not observable'.
- Size: unusual move -0.39 % (t -0.63, the cases of one day together: 2 days) per case over 1 bars, -0.098 of the coin's usual move (6.78 %); normal drift in its direction +0.54 %, total +0.16 %; 2 cases
Plan: `steps_cards/03_test_plan/night8_choppycalm_run/plans/066-01_falling-agitated-sixty-day-scaled-fall-rebound_1d.md`
Record: `steps_cards/04_backtest/night8_choppycalm_run/unseen_2016_2017/backtests/066-01_falling-agitated-sixty-day-scaled-fall-rebound_1d`
Measure: `measure.py`
