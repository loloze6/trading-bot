---
plan: 067-02.b2.b2.d2_choppy-month-fall-quickening-swing_1d
idea: 067-02.b2.b2.d2_choppy-month-fall-quickening-swing
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean position-weighted excess 10-bar fall: 0.020391; t of the mean (cases of a day summed): 1.13811 (threshold: confirm: mean > 0 with t >= 2 and supporting check passes; reject: mean < 0 with t <= -2)
- Supporting check: mean excess fall, larger |forecast| half minus smaller half: 0.0439175, passed: True
- Counts: distinct case days: 78, cases: 173
- Decided by: The t lies between -2 and 2 (or cannot be computed), which the plan calls inconclusive.
- Reading: The choppy profile (|60-bar return| <= 10 %) and the swing rule (10-bar std of daily returns over the 30-bar one > 1) are recomputed from closes inside each window, using the recorded regime where the window lacks the history; the score's mean is the mean over cases while its t is the ordinary t of the per-day summed scores; the coin's mean 10-bar return is taken on the non-overlapping grid of all its windows; the larger half of the supporting check is the cases with |forecast| strictly above the median.
- Size: unusual move +1.44 % (t 1.54, the cases of one day together: 321 days) per case over 10 bars, 0.088 of the coin's usual move (16.82 %); normal drift in its direction -1.48 %, total -0.04 %; 477 cases
Plan: `steps_cards/03_test_plan/night9_chopmonth_run/plans/067-02.b2.b2.d2_choppy-month-fall-quickening-swing_1d.md`
Record: `steps_cards/04_backtest/night9_chopmonth_run/backtests/067-02.b2.b2.d2_choppy-month-fall-quickening-swing_1d`
Measure: `measure.py`
