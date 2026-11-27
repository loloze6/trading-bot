---
plan: 066-01_falling-agitated-sixty-day-scaled-fall-rebound_1d
idea: 066-01_falling-agitated-sixty-day-scaled-fall-rebound
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: forecast-weighted mean next-day return minus coin's mean daily return: 0.00828583; t of weighted mean, same-day cases summed: 1.68806 (threshold: confirm: > 0 with t >= 2 and slope > 0; reject: t <= -2)
- Supporting check: OLS slope of excess next-day return on forecast: 0.000535508, passed: True
- Counts: cases: 4186, distinct days: 1011, active bars: 4227
- Decided by: The t lies between -2 and 2, so the result is inconclusive.
- Reading: The falling agitated profile is read from the recorded regime (the only regime with a strategy, 'unknown', is the one where both profile vetoes passed). A falling day is a negative raw scaled return, or a negative close-to-close return when the raw value is missing. The coin's mean daily return is the mean of all its within-window close-to-close returns. The t of the weighted mean sums the cases' weighted deviations f*(x-m) per UTC day and uses SE = sqrt(D/(D-1) * sum of squared day sums) / sum(f). The plan's minimum counts are taken as 100 cases and 50 distinct days, and missing them gives 'not observable'.
- Size: unusual move +0.61 % (t 1.63, the cases of one day together: 447 days) per case over 1 bars, 0.122 of the coin's usual move (5.12 %); normal drift in its direction +0.11 %, total +0.73 %; 1418 cases
Plan: `steps_cards/03_test_plan/night8_choppycalm_run/plans/066-01_falling-agitated-sixty-day-scaled-fall-rebound_1d.md`
Record: `steps_cards/04_backtest/night8_choppycalm_run/common/backtests/066-01_falling-agitated-sixty-day-scaled-fall-rebound_1d`
Measure: `measure.py`
