---
plan: 058-01_rising-calm-dip-rebound_1d
idea: 058-01_rising-calm-dip-rebound
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of the slope of 5-bar excess forward return on forecast, grid cells with forecast > 0, same-day cells pooled: 0.000416406; day-clustered OLS slope t: 0.330579 (threshold: confirm: slope t >= 2 with mean excess > 0; reject: slope t <= -2; otherwise inconclusive; at least 30 grid cases)
- Supporting check: mean excess 5-bar return > 0: -0.000703601, passed: False
- Counts: grid cases with forecast > 0: 238, days: 127
- Decided by: Inconclusive: the slope's t is between -2 and 2.
- Reading: The rising calm profile is read from the recorded regime (the bars the vetoes left as 'unknown', since the detector's components are not recorded and its 365-day lookback cannot be rebuilt inside a window), the fall from the sign of the raw pullback value; the coin's mean 5-bar return is the mean over all its windows' non-overlapping grid cells; 'same-day cells pooled' is a day-clustered (CR1) standard error of the OLS slope; the plan's 30-case minimum not reached is reported as not observable.
- Size: unusual move +0.36 % (t 0.54, the cases of one day together: 307 days) per case over 5 bars, 0.033 of the coin's usual move (10.60 %); normal drift in its direction +0.62 %, total +0.98 %; 435 cases
Plan: `steps_cards/03_test_plan/night8_risingcalm_run/plans/058-01_rising-calm-dip-rebound_1d.md`
Record: `steps_cards/04_backtest/night8_risingcalm_run/backtests/058-01_rising-calm-dip-rebound_1d`
Measure: `measure.py`
