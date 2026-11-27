---
plan: 064-01.g1.b1_calm-decline-big-rise-next-day-fade_1d
idea: 064-01.g1.b1_calm-decline-big-rise-next-day-fade
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual next-day move of short bets (short direction): 0.00288821; t of the mean, cases of one day taken together: 0.994358 (threshold: confirm: mean > 0 with t >= 2 and supporting check passes; reject: t <= -2)
- Supporting check: upper-half minus lower-half mean unusual move, split at median scaled rise: 0.00496936, passed: True
- Counts: cases: 321, distinct days: 201
- Decided by: The t lies between -2 and 2.
- Reading: The situation is checked as raw scaled rise (recorded last_history_value, else recomputed from closes) >= 1 on a bar whose regime is mean_reversion (the falling-calm profile vetoes send other bars to chop, and the profile's 60-day/365-day inputs cannot be rebuilt inside the ~120-bar windows), with a negative forecast; cases are bars where the short forecast deepens by at least 2 points from its shallowest level since the last bet (from 0 after flat), the drift is the coin's mean daily return over all its windows, and the median split puts cases above the median in the upper half and those at or below it in the lower half.
- Size: unusual move +0.29 % (t 1.00, the cases of one day together: 201 days) per case over 1 bars, 0.057 of the coin's usual move (4.73 %); normal drift in its direction -0.13 %, total +0.16 %; 321 cases
Plan: `steps_cards/03_test_plan/night9_fallcalmfade_run/plans/064-01.g1.b1_calm-decline-big-rise-next-day-fade_1d.md`
Record: `steps_cards/04_backtest/night9_fallcalmfade_run/backtests/064-01.g1.b1_calm-decline-big-rise-next-day-fade_1d`
Measure: `measure.py`
