---
plan: 060-01_falling-agitated-high-close-fade_1d
idea: 060-01_falling-agitated-high-close-fade
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-side next-day excess return over the coin's mean: 0.00201314; t of the mean, cases of one day summed: 0.775719 (threshold: confirm: mean > 0 with t >= 2 and supporting check > 0; reject: mean < 0 with t <= -2)
- Supporting check: mean excess of larger-|forecast| half minus smaller half: 0.00551419, passed: True
- Counts: cases: 1051, distinct days: 534
- Decided by: The t of the mean short-side excess lies between -2 and 2.
- Reading: The falling-agitated profile is taken from the detector's recorded regime 'mean_reversion' (its profile components are not recorded and their 365-bar lookback cannot be rebuilt inside a window), the close location from the recorded raw value or the prices; the coin's mean daily return is the mean of all its in-window next-bar returns; the day-clustered t uses per-day summed deviations with a n_days/(n_days-1) correction; the supporting split puts cases with |forecast| above the median in the larger half and the rest in the smaller.
- Size: unusual move +0.36 % (t 1.33, the cases of one day together: 412 days) per case over 1 bars, 0.068 of the coin's usual move (5.16 %); normal drift in its direction -0.09 %, total +0.27 %; 740 cases
Plan: `steps_cards/03_test_plan/a4_research_run/plans/060-01_falling-agitated-high-close-fade_1d.md`
Record: `steps_cards/04_backtest/a4_research_run/backtests/060-01_falling-agitated-high-close-fade_1d`
Measure: `measure.py`
