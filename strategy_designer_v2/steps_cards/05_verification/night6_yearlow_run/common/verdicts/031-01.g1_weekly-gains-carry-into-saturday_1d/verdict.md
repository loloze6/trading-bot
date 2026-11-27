---
plan: 031-01.g1_weekly-gains-carry-into-saturday_1d
idea: 031-01.g1_weekly-gains-carry-into-saturday
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of forecast/10 x (next-bar return - coin mean daily return), trending bars with forecast > 0: 0.0067432; t of the mean, cases of one day summed: 2.87771 (threshold: confirm: above 0 with t >= 2 (and supporting check positive); reject: below 0 with t <= -2)
- Supporting check: Saturday excess return, top third of positive Friday forecasts minus Friday forecast 0: 0.0102582, passed: True
- Counts: distinct days with a positive forecast: 496, main measure cases: 3899, days of main measure cases: 493, top-third Friday bars: 1300, zero-forecast Friday bars: 4094
- Decided by: The main measure is above 0 with t >= 2 and the supporting check is positive.
- Reading: The coming bar is the bar opening at timestamp + 1 day, so the situation is a Friday-UTC bar with a positive 5-bar return (recorded raw value, else recomputed in-window), expected long; Friday bars for the supporting check are those same bars; the top third is above the 2/3 quantile of positive Friday forecasts pooled over coins; the day-clustered t sums deviations per UTC date with a D/(D-1) correction; distinct days with a positive forecast count UTC dates of any bar with forecast > 0.
- Size: unusual move +0.63 % (t 3.46, the cases of one day together: 467 days) per case over 1 bars, 0.115 of the coin's usual move (5.44 %); normal drift in its direction +0.15 %, total +0.78 %; 3357 cases
- Direction check on folds A, D (the years step 7 does not explore): not judged: no check fold (the plan has none, or the backtest did not run on its folds)
Plan: `steps_cards/03_test_plan/night6_yearlow_run/plans/031-01.g1_weekly-gains-carry-into-saturday_1d.md`
Record: `steps_cards/04_backtest/night6_yearlow_run/common/backtests/031-01.g1_weekly-gains-carry-into-saturday_1d`
Measure: `measure.py`
