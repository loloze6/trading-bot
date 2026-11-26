---
plan: 060-01.g1.d1_wider-than-usual-high-close-fade_1d
idea: 060-01.g1.d1_wider-than-usual-high-close-fade
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-side unusual 1-bar move per case: 0.00801093; t of the mean, cases summed per day: 1.89077 (threshold: confirm: mean > 0 with t >= 2 (cases summed per day) and supporting check passes; reject: mean < 0 with t <= -2)
- Supporting check: wider-half minus narrower-half mean move (split at median range_mult): 0.0076742, passed: True
- Counts: cases: 347, case-days: 212, active bars: 379
- Decided by: t lies between -2 and 2
- Reading: The falling agitated profile is not recomputed (its detector components are not recorded and need more history than a window) so the check covers the upper-half close and range multiple >= 1 on the short side; the wider half is cases strictly above the median range_mult and the narrower half those at or below it; the plan's 'fewer than 30 cases or case-days' rule is reported as not observable.
- Size: unusual move +0.80 % (t 1.90, the cases of one day together: 212 days) per case over 1 bars, 0.165 of the coin's usual move (4.73 %); normal drift in its direction -0.13 %, total +0.67 %; 347 cases
Plan: `steps_cards/03_test_plan/night8_risingagitated_run/plans/060-01.g1.d1_wider-than-usual-high-close-fade_1d.md`
Record: `steps_cards/04_backtest/night8_risingagitated_run/backtests/060-01.g1.d1_wider-than-usual-high-close-fade_1d`
Measure: `measure.py`
