---
plan: 072-04_choppy-deep-close-multiday-fall_1d
idea: 072-04_choppy-deep-close-multiday-fall
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of excess 3-bar forward return (minus coin's normal drift) on forecast, pooled, day-clustered: -2.34659e-05; OLS t clustered by day: -0.054057 (threshold: confirm: slope > 0 with t >= 2 (and deepest third mean excess < 0); reject: slope < 0 with t <= -2; else inconclusive)
- Supporting check: deepest third of forecasts: mean excess 3-bar return below 0: -0.00122199, passed: True
- Counts: non-overlapping cases: 1398, distinct days: 634
- Decided by: The slope's |t| is below 2 (inconclusive rule).
- Reading: Choppy profile read from the recorded regime (the config's strategy regime 'unknown', since the detector's PriceEvolution component is not recorded), close below the 20-day high as raw depth < 0, expected side short (forecast < 0); slope t is OLS with intercept, CR1 cluster-robust by UTC day; the deepest third is the floor(n/3) cases with the most negative forecasts; the plan's minimum counts (100 cases, 60 days) are applied as 'not observable' when not reached.
- Size: unusual move +0.10 % (t 0.41, the cases of one day together: 885 days) per case over 3 bars, 0.025 of the coin's usual move (7.96 %); normal drift in its direction -0.35 %, total -0.25 %; 1261 cases
Plan: `steps_cards/03_test_plan/night9_chopdeep_run/plans/072-04_choppy-deep-close-multiday-fall_1d.md`
Record: `steps_cards/04_backtest/night9_chopdeep_run/backtests/072-04_choppy-deep-close-multiday-fall_1d`
Measure: `measure.py`
