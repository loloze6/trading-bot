---
plan: 058-02.b1.b2.b1.b2.b2.e1_calm-range-edge-short-continuation_1d
idea: 058-02.b1.b2.b1.b2.b2.e1_calm-range-edge-short-continuation
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of slope of 2-bar forward return minus normal drift on range_pos post_pipeline_value (day-clustered): 2.582; day-clustered OLS slope t: 2.582 (threshold: confirm t >= 2 with timing gain > 0; reject t <= -2; inconclusive otherwise or < 300 grid cases or < 100 distinct days)
- Supporting check: timing gain: book mean daily return minus market-rise gain, before costs: 0.000834724, passed: True
- Counts: grid cases: 12699, distinct days: 1668
- Decided by: The slope's t is 2 or more and the timing gain is above 0.
- Reading: Calm is the regime 'unknown', the expected side is the close above/below the middle of its 20-bar high-low range; the normal drift is the coin's mean 2-bar return on all grid bars of all its windows; the regression has an intercept with CR1 day-clustered errors; the book before costs is the held allocation times the next bar's close-to-close return, averaged over coins per day.
- Size: unusual move +0.36 % (t 2.75, the cases of one day together: 2263 days) per case over 2 bars, 0.052 of the coin's usual move (7.28 %); normal drift in its direction +0.00 %, total +0.37 %; 8047 cases
- Direction check on folds A, D (the years step 7 does not explore): not judged: no check fold (the plan has none, or the backtest did not run on its folds)
Plan: `steps_cards/03_test_plan/night8_choppycalm_run/plans/058-02.b1.b2.b1.b2.b2.e1_calm-range-edge-short-continuation_1d.md`
Record: `steps_cards/04_backtest/night8_choppycalm_run/common/backtests/058-02.b1.b2.b1.b2.b2.e1_calm-range-edge-short-continuation_1d`
Measure: `measure.py`
