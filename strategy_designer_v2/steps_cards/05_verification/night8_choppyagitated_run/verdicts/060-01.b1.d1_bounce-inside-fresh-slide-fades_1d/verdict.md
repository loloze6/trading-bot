---
plan: 060-01.b1.d1_bounce-inside-fresh-slide-fades_1d
idea: 060-01.b1.d1_bounce-inside-fresh-slide-fades
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 3-bar move after short bets, in the short direction: 0.00552629; t with same-day cases pooled: 1.08055 (threshold: mean > 0 with day-pooled t >= 2 to confirm; mean < 0 with t <= -2 to reject)
- Supporting check: large-minus-small (median |forecast|) mean unusual move, Welch t: 0.0016273, passed: True
- Counts: cases: 1039, distinct days: 380
- Decided by: Inconclusive: the main t lies between -2 and 2.
- Reading: A case is the first short bet (|forecast| rise of >= 2 points from its lowest level since the last bet) in each 3-bar grid cell of a window, its 3-bar return taken from that bar's close; the median split puts |forecast| above the median in the larger group and the rest in the smaller; the plan's 'else inconclusive' for too few cases is reported as 'not observable' per the workflow; the day-pooled t sums deviations per UTC day with a G/(G-1) correction.
- Size: unusual move +0.55 % (t 1.08, the cases of one day together: 380 days) per case over 3 bars, 0.067 of the coin's usual move (8.85 %); normal drift in its direction -0.43 %, total +0.12 %; 1039 cases
Plan: `steps_cards/03_test_plan/night8_choppyagitated_run/plans/060-01.b1.d1_bounce-inside-fresh-slide-fades_1d.md`
Record: `steps_cards/04_backtest/night8_choppyagitated_run/backtests/060-01.b1.d1_bounce-inside-fresh-slide-fades_1d`
Measure: `measure.py`
