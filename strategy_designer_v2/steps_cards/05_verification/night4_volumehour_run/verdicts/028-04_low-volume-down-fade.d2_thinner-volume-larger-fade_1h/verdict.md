---
plan: 028-04_low-volume-down-fade.d2_thinner-volume-larger-fade_1h
idea: 028-04_low-volume-down-fade.d2_thinner-volume-larger-fade
fit: adapted
status: inconclusive
---
Situation check: 96 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 6-bar unusual move after long bets (return minus coin's normal 6-bar drift), before costs: 0.000334453; t of the mean: 2.09008 (threshold: confirm: mean > 0 with t >= 2 and thin-minus-heavy > 0; reject: mean < 0 with t <= -2)
- Supporting check: mean unusual move, thinner-volume half minus heavier-volume half: -0.000222528, passed: False
- Counts: long cases pooled over both coins and all windows: 16868, thinner-volume half: 8434, heavier-volume half: 8434
- Decided by: t >= 2 but the thin-minus-heavy difference is <= 0 (or not measurable), which the plan calls inconclusive.
- Reading: Situation taken as a down hour (raw fall < 0, or the price return where unrecorded) with a positive forecast; bets per the holding-period rule with one case per 6-bar cell; volume halves split as v <= median (thinner) versus v > median (heavier), cases without a valid v left out of the split.
- Size: unusual move +0.03 % per case over 6 bars, 0.016 of the coin's usual move (1.98 %); normal drift in its direction +0.03 %, total +0.06 %; 17160 cases
Plan: `steps_cards/03_test_plan/night4_volumehour_run/plans/028-04_low-volume-down-fade.d2_thinner-volume-larger-fade_1h.md`
Record: `steps_cards/04_backtest/night4_volumehour_run/backtests/028-04_low-volume-down-fade.d2_thinner-volume-larger-fade_1h`
Measure: `measure.py`
