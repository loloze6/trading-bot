---
plan: 066-01_falling-agitated-sixty-day-scaled-fall-rebound_1d
idea: 066-01_falling-agitated-sixty-day-scaled-fall-rebound
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: forecast-weighted mean next-day return minus coin's mean daily return: 0.0101253; t of weighted mean, same-day cases summed: 2.05511 (threshold: confirm: > 0 with t >= 2 and slope > 0; reject: t <= -2)
- Supporting check: OLS slope of excess next-day return on forecast: 0.00052244, passed: True
- Counts: cases: 2865, distinct days: 830, active bars: 2897
- Decided by: The forecast-weighted mean excess return is above 0 with t >= 2, and the slope is positive.
- Reading: The falling agitated profile is read from the recorded regime (the only regime with a strategy, 'unknown', is the one where both profile vetoes passed). A falling day is a negative raw scaled return, or a negative close-to-close return when the raw value is missing. The coin's mean daily return is the mean of all its within-window close-to-close returns. The t of the weighted mean sums the cases' weighted deviations f*(x-m) per UTC day and uses SE = sqrt(D/(D-1) * sum of squared day sums) / sum(f). The plan's minimum counts are taken as 100 cases and 50 distinct days, and missing them gives 'not observable'.
- Size: unusual move +0.93 % (t 2.28, the cases of one day together: 358 days) per case over 1 bars, 0.193 of the coin's usual move (5.33 %); normal drift in its direction +0.13 %, total +1.06 %; 987 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.004413 on the check folds against +0.01013 on every fold
Plan: `steps_cards/03_test_plan/night8_choppycalm_run/plans/066-01_falling-agitated-sixty-day-scaled-fall-rebound_1d.md`
Record: `steps_cards/04_backtest/night8_choppycalm_run/backtests/066-01_falling-agitated-sixty-day-scaled-fall-rebound_1d`
Measure: `measure.py`
