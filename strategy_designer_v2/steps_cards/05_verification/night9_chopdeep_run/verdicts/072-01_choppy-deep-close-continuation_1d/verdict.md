---
plan: 072-01_choppy-deep-close-continuation_1d
idea: 072-01_choppy-deep-close-continuation
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of next-day return minus coin mean on abs(depth post_pipeline_value): 1.66576e-05; OLS t, SE clustered by day: 0.0985735 (threshold: confirm: slope < 0 with clustered t <= -2 (and check passes); reject: slope > 0 with t >= 2)
- Supporting check: slope below 0 on up-close and on down-close bars (larger of the two slopes shown): 8.45569e-05, passed: False
- Counts: in-profile bars: 4219, distinct days: 1901, up-day bars: 2184, down-day bars: 2029
- Decided by: The slope's |t| is below 2 (inconclusive rule).
- Reading: The choppy profile is read as the bars whose regime is 'unknown' (the config's only regime with a strategy, flat when the 60-day trend veto says 'chop'), the situation as that regime with a raw depth below 0 and a short forecast; 'the day closed up/down' is close above/below the same bar's open; the minimum counts are taken on the regression's sample (non-zero forecast with a next-day return and a depth value), days being UTC calendar dates.
- Size: unusual move -0.08 % (t -0.61, the cases of one day together: 991 days) per case over 1 bars, -0.008 of the coin's usual move (4.78 %); normal drift in its direction -0.12 %, total -0.20 %; 1487 cases
Plan: `steps_cards/03_test_plan/night9_chopdeep_run/plans/072-01_choppy-deep-close-continuation_1d.md`
Record: `steps_cards/04_backtest/night9_chopdeep_run/backtests/072-01_choppy-deep-close-continuation_1d`
Measure: `measure.py`
