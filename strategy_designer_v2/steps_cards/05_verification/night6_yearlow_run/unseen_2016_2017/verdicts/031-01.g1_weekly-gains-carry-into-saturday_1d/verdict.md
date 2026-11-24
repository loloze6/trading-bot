---
plan: 031-01.g1_weekly-gains-carry-into-saturday_1d
idea: 031-01.g1_weekly-gains-carry-into-saturday
fit: adapted
status: not observable
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of forecast/10 x (next-bar return - coin mean daily return), trending bars with forecast > 0: 0.00335543; t of the mean, cases of one day summed: 0.541782 (threshold: confirm: above 0 with t >= 2 (and supporting check positive); reject: below 0 with t <= -2)
- Supporting check: Saturday excess return, top third of positive Friday forecasts minus Friday forecast 0: 0.0156066, passed: True
- Counts: distinct days with a positive forecast: 98, main measure cases: 256, days of main measure cases: 98, top-third Friday bars: 85, zero-forecast Friday bars: 164
- Decided by: Only 98 distinct days with a positive forecast, below the plan's minimum of 300.
- Reading: The coming bar is the bar opening at timestamp + 1 day, so the situation is a Friday-UTC bar with a positive 5-bar return (recorded raw value, else recomputed in-window), expected long; Friday bars for the supporting check are those same bars; the top third is above the 2/3 quantile of positive Friday forecasts pooled over coins; the day-clustered t sums deviations per UTC date with a D/(D-1) correction; distinct days with a positive forecast count UTC dates of any bar with forecast > 0.
- Size: unusual move +0.30 % (t 0.48, the cases of one day together: 90 days) per case over 1 bars, 0.056 of the coin's usual move (7.55 %); normal drift in its direction +0.96 %, total +1.25 %; 215 cases
Plan: `steps_cards/03_test_plan/night6_yearlow_run/plans/031-01.g1_weekly-gains-carry-into-saturday_1d.md`
Record: `steps_cards/04_backtest/night6_yearlow_run/unseen_2016_2017/backtests/031-01.g1_weekly-gains-carry-into-saturday_1d`
Measure: `measure.py`
