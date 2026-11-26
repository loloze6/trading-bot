---
plan: 060-01.g1.d2.g1_up-day-high-close-fade_1d
idea: 060-01.g1.d2.g1_up-day-high-close-fade
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-side unusual next-bar move after short-forecast rises of >= 2 points: 0.00632021; t of the mean, cases of one day taken together: 2.35839 (threshold: confirm: mean > 0 with t >= 2 and supporting check passes; reject: mean < 0 with t <= -2)
- Supporting check: upper-half minus lower-half mean unusual move, split at median close location: -0.0050525, passed: False
- Counts: cases: 840, distinct days of cases: 444
- Decided by: Positive main result with t >= 2 but the supporting check (upper minus lower half above 0) fails.
- Reading: The falling-agitated profile (60-bar trend and 365-bar volatility percentile) cannot be rebuilt inside ~122-bar windows, so the situation check tests the up close (close above prior close in the same window, first bars left out) and close location > 0.5 with a short forecast; the day-clustered t uses per-day summed deviations with a G/(G-1) correction, and the median split puts locations above the median in the upper half and the rest in the lower half.
- Size: unusual move +0.63 % (t 2.36, the cases of one day together: 444 days) per case over 1 bars, 0.134 of the coin's usual move (4.73 %); normal drift in its direction -0.13 %, total +0.50 %; 840 cases
Plan: `steps_cards/03_test_plan/night8_risingagitated_run/plans/060-01.g1.d2.g1_up-day-high-close-fade_1d.md`
Record: `steps_cards/04_backtest/night8_risingagitated_run/backtests/060-01.g1.d2.g1_up-day-high-close-fade_1d`
Measure: `measure.py`
