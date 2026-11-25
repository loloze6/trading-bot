---
plan: 046-01_falling-market-scaled-rise-fade_1d
idea: 046-01_falling-market-scaled-rise-fade
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: |forecast|-weighted mean next-day unusual move, short direction: 0.0027919; t of the weighted mean, cases of one day summed: 1.51186 (threshold: confirm: > 0 with t >= 2 and positive slope; reject: < 0 with t <= -2; else inconclusive)
- Supporting check: slope of next-day excess return on forecast over the cases: -2.37305e-05, passed: False
- Counts: cases: 2951, case days: 1126
- Decided by: The main t lies between -2 and 2, which the plan calls inconclusive.
- Reading: The falling profile is read from the recorded regime (the detector's decision: 'unknown' = 60-bar price change below -10, the only regime with a strategy) since the detector's component is not recorded, the up day is a positive raw scaled_rise value (the bar's own in-window return where it is missing), the 100-case minimum counts coin-bar cases with forecast < 0 and a next-day return, and the day-clustered t sums each day's weighted deviations w*(u - mean) over sum(w).
- Size: unusual move +0.25 % (t 1.42, the cases of one day together: 860 days) per case over 1 bars, 0.058 of the coin's usual move (4.78 %); normal drift in its direction -0.12 %, total +0.13 %; 1963 cases
Plan: `steps_cards/03_test_plan/night7_panic_run/plans/046-01_falling-market-scaled-rise-fade_1d.md`
Record: `steps_cards/04_backtest/night7_panic_run/backtests/046-01_falling-market-scaled-rise-fade_1d`
Measure: `measure.py`
