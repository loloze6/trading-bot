---
plan: 058-01.b1.b1.b2_large-rallies-fail-within-week_1d
idea: 058-01.b1.b1.b2_large-rallies-fail-within-week
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of 5-bar excess return (minus coin's normal 5-bar drift) on forecast, cases forecast < 0: 0.000931501; t clustered by day: 0.93419 (threshold: confirm: slope > 0 with t >= 2 (and supporting check); reject: slope < 0 with t <= -2; else inconclusive)
- Supporting check: mean 5-bar excess return in the short direction > 0: 0.0137688, passed: True
- Counts: distinct days of cases: 151, cases: 493
- Decided by: The slope's clustered t lies between -2 and 2 (inconclusive rule).
- Reading: The falling-agitated profile is read as regime == 'unknown' (the detector's recorded decision, the only regime with a strategy), the situation as a positive raw scaled 3-day rise (prices' 3-day return where not recorded) with forecast < 0; the drift is the coin's mean 5-bar return on all its windows' grids; the plan's 'fewer than 30 distinct days' is treated as its minimum count (not observable); clustered t uses the CR1 small-sample correction.
- Size: unusual move +0.86 % (t 1.24, the cases of one day together: 290 days) per case over 5 bars, 0.066 of the coin's usual move (11.68 %); normal drift in its direction -0.74 %, total +0.12 %; 701 cases
Plan: `steps_cards/03_test_plan/night8_fallingagitated_run/plans/058-01.b1.b1.b2_large-rallies-fail-within-week_1d.md`
Record: `steps_cards/04_backtest/night8_fallingagitated_run/backtests/058-01.b1.b1.b2_large-rallies-fail-within-week_1d`
Measure: `measure.py`
