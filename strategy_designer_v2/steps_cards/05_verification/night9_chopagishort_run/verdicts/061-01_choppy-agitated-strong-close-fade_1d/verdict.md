---
plan: 061-01_choppy-agitated-strong-close-fade_1d
idea: 061-01_choppy-agitated-strong-close-fade
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 2-bar move of short signals, short direction: 0.00651057; t of the mean, cases pooled by day: 1.49341 (threshold: confirm: mean > 0 with t >= 2 over at least 30 cases; reject: t <= -2 over at least 30 cases)
- Supporting check: mean unusual move (loc >= 0.9) minus (0.8 <= loc < 0.9): 0.0038794, passed: True
- Counts: cases: 233, days: 194, cases loc >= 0.9: 106, cases loc 0.8-0.9: 127
- Decided by: The t is between -2 and 2.
- Reading: The situation is checked as the close location recomputed from each bar's high, low and close being at least 0.8 with a negative forecast (the choppy-agitated profile is the config's veto, not recomputed); a case is a short bet (the forecast's short size rising by at least 2 points from its lowest short level since the last bet, from 0 after flat or long), the first per 2-bar grid cell of each window; the drift is each coin's mean non-overlapping 2-bar return over all its windows; the t is the mean over a day-clustered standard error; an empty close-location group makes the supporting check fail.
- Size: unusual move +0.65 % (t 1.50, the cases of one day together: 194 days) per case over 2 bars, 0.129 of the coin's usual move (6.58 %); normal drift in its direction -0.25 %, total +0.40 %; 233 cases
Plan: `steps_cards/03_test_plan/night9_chopagishort_run/plans/061-01_choppy-agitated-strong-close-fade_1d.md`
Record: `steps_cards/04_backtest/night9_chopagishort_run/backtests/061-01_choppy-agitated-strong-close-fade_1d`
Measure: `measure.py`
