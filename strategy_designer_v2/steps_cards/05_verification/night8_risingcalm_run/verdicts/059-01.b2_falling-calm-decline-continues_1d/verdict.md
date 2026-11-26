---
plan: 059-01.b2_falling-calm-decline-continues_1d
idea: 059-01.b2_falling-calm-decline-continues
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of 5-day excess return on forecast (forecast < 0, day-clustered): 0.00123013; day-clustered OLS t of the slope: 1.21501 (threshold: confirm: slope > 0 with t >= 2 (and mean excess < 0); reject: slope < 0 with t <= -2)
- Supporting check: mean 5-day excess return on the forecast < 0 grid bars: -0.00583015, passed: True
- Counts: grid cases: 438, distinct days: 194
- Decided by: Inconclusive: the slope has |t| < 2.
- Reading: The falling calm profile is read from the recorded regime (regime 'unknown', the only regime with a strategy, i.e. both vetoes not triggered) and the decline from the raw scaled 14-day return < 0, expected side short; the coin's mean 5-day return is the mean over its non-overlapping grid (positions 0, 5, 10, ... of each window) of all windows; the slope is OLS with intercept and day-clustered standard errors with the usual G/(G-1)*(N-1)/(N-K) correction; minimum counts not reached give 'not observable'.
- Size: unusual move +1.28 % (t 2.29, the cases of one day together: 350 days) per case over 5 bars, 0.116 of the coin's usual move (10.60 %); normal drift in its direction -0.65 %, total +0.63 %; 512 cases
Plan: `steps_cards/03_test_plan/night8_risingcalm_run/plans/059-01.b2_falling-calm-decline-continues_1d.md`
Record: `steps_cards/04_backtest/night8_risingcalm_run/backtests/059-01.b2_falling-calm-decline-continues_1d`
Measure: `measure.py`
