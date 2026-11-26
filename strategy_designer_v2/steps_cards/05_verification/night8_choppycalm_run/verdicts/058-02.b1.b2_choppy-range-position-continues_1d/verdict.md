---
plan: 058-02.b1.b2_choppy-range-position-continues_1d
idea: 058-02.b1.b2_choppy-range-position-continues
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope of 5-day forward return minus coin mean 5-day return on range_pos post_pipeline_value: 0.000230954; OLS slope t: 0.868905 (threshold: confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; else inconclusive)
- Supporting check: none
- Counts: active bars: 4256, grid cases inside the profile: 819
- Decided by: the slope's t lies between -2 and +2 (inconclusive rule)
- Reading: the choppy profile is the bars where range_pos is recorded and the expected side is the sign of its raw range position; the grid starts at each window's first row, the coin's mean 5-day return is taken over all its grid returns in all windows, the slope is a pooled OLS with intercept on all recorded grid bars (including zero values), and its t is slope over its standard error.
- Size: unusual move +0.27 % (t 0.90, the cases of one day together: 829 days) per case over 5 bars, 0.021 of the coin's usual move (10.60 %); normal drift in its direction -0.00 %, total +0.27 %; 1153 cases
Plan: `steps_cards/03_test_plan/night8_choppycalm_run/plans/058-02.b1.b2_choppy-range-position-continues_1d.md`
Record: `steps_cards/04_backtest/night8_choppycalm_run/backtests/058-02.b1.b2_choppy-range-position-continues_1d`
Measure: `measure.py`
