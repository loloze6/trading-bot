---
plan: 060-01.g1.g1_graded-width-high-close-fade_1d
idea: 060-01.g1.g1_graded-width-high-close-fade
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess next-day fall on short cases (short direction, vs coin drift): 0.00406483; t of the mean, cases summed per day: 1.83107 (threshold: confirm: mean > 0 with t >= 2 and supporting check passes; reject: t <= -2; else inconclusive; >= 100 cases on >= 50 days)
- Supporting check: above-median |forecast| mean excess fall minus below-median: 0.00622419, passed: True
- Counts: cases: 1380, distinct days: 669
- Decided by: The t lies between -2 and 2, which the plan calls inconclusive.
- Reading: The profile part of the situation (falling agitated) cannot be rebuilt from prices inside ~120-bar windows (365-bar lookback), so it is read from the recorded regime not being the veto result 'chop', while the upper-half close is recomputed from prices as (close-low)/(high-low) > 0.5; cases on the same UTC day are summed and the t uses a day-clustered standard error of the case mean; the supporting check splits cases strictly above and strictly below the median of |forecast| (ties at the median left out); the last bar of each window has no next-day return and is left out.
- Size: unusual move +0.55 % (t 2.13, the cases of one day together: 501 days) per case over 1 bars, 0.113 of the coin's usual move (4.73 %); normal drift in its direction -0.13 %, total +0.42 %; 954 cases
Plan: `steps_cards/03_test_plan/night8_risingagitated_run/plans/060-01.g1.g1_graded-width-high-close-fade_1d.md`
Record: `steps_cards/04_backtest/night8_risingagitated_run/backtests/060-01.g1.g1_graded-width-high-close-fade_1d`
Measure: `measure.py`
