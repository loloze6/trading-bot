---
plan: 058-01_agitated-rise-stretch-giveback_1d
idea: 058-01_agitated-rise-stretch-giveback
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of the OLS slope of 5-bar excess return (vs normal drift) on abs(forecast), short grid cases: 0.394592; OLS slope t: 0.394592 (threshold: confirm: slope < 0 with t <= -2 and mean short unusual move > 0; reject: slope > 0 with t >= +2; else inconclusive)
- Supporting check: mean unusual move in the short direction (minus excess return): -0.0107829, passed: False
- Counts: independent short cases: 436
- Decided by: The slope's |t| is below 2.
- Reading: The rising agitated profile is read from the recorded regime (the only regime with a strategy, 'unknown', i.e. not vetoed to chop) since the detector's components are not recorded, the distance from last_history_value (recomputed from in-window prices where missing), the normal drift as each coin's mean 5-bar return on the non-overlapping grid of all its windows, and the plan's 'fewer than 30 independent short cases' minimum is treated as a minimum count giving 'not observable'.
- Size: unusual move -0.81 % (t -1.06, the cases of one day together: 320 days) per case over 5 bars, -0.072 of the coin's usual move (10.60 %); normal drift in its direction -0.64 %, total -1.44 %; 436 cases
Plan: `steps_cards/03_test_plan/night8_risingagitated_run/plans/058-01_agitated-rise-stretch-giveback_1d.md`
Record: `steps_cards/04_backtest/night8_risingagitated_run/backtests/058-01_agitated-rise-stretch-giveback_1d`
Measure: `measure.py`
