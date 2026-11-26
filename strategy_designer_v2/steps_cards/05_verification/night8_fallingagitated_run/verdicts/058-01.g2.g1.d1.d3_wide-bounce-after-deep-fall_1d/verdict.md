---
plan: 058-01.g2.g1.d1.d3_wide-bounce-after-deep-fall_1d
idea: 058-01.g2.g1.d1.d3_wide-bounce-after-deep-fall
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-direction next-day excess return on bars with forecast <= -2: 0.00508779; t of the mean, cases summed per day: 1.62761 (threshold: confirm: mean > 0 with t >= 2 on at least 100 cases; reject: mean < 0 with t <= -2 on at least 100 cases)
- Supporting check: top-half minus bottom-half (by |forecast|) mean short excess return, Welch t: 0.00531633, passed: True
- Counts: cases: 792, days with cases: 406, top-half cases: 396, bottom-half cases: 396
- Decided by: Inconclusive: the main t is between -2 and 2 and no reject rule is met.
- Reading: The situation is checked as a 1-day close-to-close return > 0 and a negative 3-day return ending the previous bar (recorded fall_depth raw value, else recomputed from closes), bars whose prior close is outside the window left out, profile not required; the coin mean is the mean of all its 1-bar returns over all windows; the main t clusters case deviations summed per UTC day; the top half is |forecast| above the cases' median, the bottom half at or below it.
- Size: unusual move +0.77 % (t 2.36, the cases of one day together: 333 days) per case over 1 bars, 0.163 of the coin's usual move (4.73 %); normal drift in its direction -0.13 %, total +0.64 %; 630 cases
Plan: `steps_cards/03_test_plan/night8_fallingagitated_run/plans/058-01.g2.g1.d1.d3_wide-bounce-after-deep-fall_1d.md`
Record: `steps_cards/04_backtest/night8_fallingagitated_run/backtests/058-01.g2.g1.d1.d3_wide-bounce-after-deep-fall_1d`
Measure: `measure.py`
