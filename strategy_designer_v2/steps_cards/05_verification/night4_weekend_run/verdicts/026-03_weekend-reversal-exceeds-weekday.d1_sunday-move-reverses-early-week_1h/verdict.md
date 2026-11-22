---
plan: 026-03_weekend-reversal-exceeds-weekday.d1_sunday-move-reverses-early-week_1h
idea: 026-03_weekend-reversal-exceeds-weekday.d1_sunday-move-reverses-early-week
fit: exact
status: confirmed
---
Situation check: 99 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of next-48-bar return minus coin mean on forecast/10: 0.00319792; OLS slope t: 2.49213 (threshold: confirm: slope > 0 with t >= 2 (and support passes); reject: t <= -2)
- Supporting check: slope difference (Sunday 24h-return slope minus other-days 48h-return slope), t: -4.22955, passed: True
- Counts: Sunday cases: 2414, Sunday cases in supporting check: 2390, other weekday cases: 14360
- Decided by: Main slope positive with t >= 2 and slope difference t <= -2.
- Reading: Sunday cases are bars starting Sunday 23:00 UTC with nonzero forecast and 48 later rows in the window, the coin mean is over the non-overlapping 48-bar grid of all its windows, the supporting slopes use raw (not demeaned) next-48-bar returns with returns recomputed from closes as fractions and other-day cases at 23:00 bars Monday to Saturday, the slope-difference t is (b1-b2)/sqrt(se1^2+se2^2), and the plan's 300-case minimum yields 'not observable'.
- Size: unusual move +0.60 % per case over 48 bars, 0.095 of the coin's usual move (6.56 %); normal drift in its direction -0.01 %, total +0.59 %; 2134 cases
Plan: `steps_cards/03_test_plan/night4_weekend_run/plans/026-03_weekend-reversal-exceeds-weekday.d1_sunday-move-reverses-early-week_1h.md`
Record: `steps_cards/04_backtest/night4_weekend_run/backtests/026-03_weekend-reversal-exceeds-weekday.d1_sunday-move-reverses-early-week_1h`
Measure: `measure.py`
