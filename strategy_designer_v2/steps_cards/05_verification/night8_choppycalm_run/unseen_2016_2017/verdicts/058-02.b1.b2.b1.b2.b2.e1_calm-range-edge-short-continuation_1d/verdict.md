---
plan: 058-02.b1.b2.b1.b2.b2.e1_calm-range-edge-short-continuation_1d
idea: 058-02.b1.b2.b1.b2.b2.e1_calm-range-edge-short-continuation
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of slope of 2-bar forward return minus normal drift on range_pos post_pipeline_value (day-clustered): 0.563577; day-clustered OLS slope t: 0.563577 (threshold: confirm t >= 2 with timing gain > 0; reject t <= -2; inconclusive otherwise or < 300 grid cases or < 100 distinct days)
- Supporting check: timing gain: book mean daily return minus market-rise gain, before costs: -0.000433843, passed: False
- Counts: grid cases: 424, distinct days: 298
- Decided by: The slope's t is between -2 and 2.
- Reading: Calm is the regime 'unknown', the expected side is the close above/below the middle of its 20-bar high-low range; the normal drift is the coin's mean 2-bar return on all grid bars of all its windows; the regression has an intercept with CR1 day-clustered errors; the book before costs is the held allocation times the next bar's close-to-close return, averaged over coins per day.
- Size: unusual move -0.24 % (t -0.72, the cases of one day together: 225 days) per case over 2 bars, -0.021 of the coin's usual move (10.15 %); normal drift in its direction +0.57 %, total +0.32 %; 267 cases
Plan: `steps_cards/03_test_plan/night8_choppycalm_run/plans/058-02.b1.b2.b1.b2.b2.e1_calm-range-edge-short-continuation_1d.md`
Record: `steps_cards/04_backtest/night8_choppycalm_run/unseen_2016_2017/backtests/058-02.b1.b2.b1.b2.b2.e1_calm-range-edge-short-continuation_1d`
Measure: `measure.py`
