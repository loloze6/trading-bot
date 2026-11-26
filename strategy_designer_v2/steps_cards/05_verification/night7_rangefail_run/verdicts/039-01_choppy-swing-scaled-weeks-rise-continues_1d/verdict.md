---
plan: 039-01_choppy-swing-scaled-weeks-rise-continues_1d
idea: 039-01_choppy-swing-scaled-weeks-rise-continues
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of 5-bar forward excess return (minus coin's normal drift) on forecast, day-pooled: 0.00186308; OLS slope t (day-pooled): 1.9142 (threshold: confirm: slope t >= 2 with mean directional excess > 0; reject: slope t <= -2)
- Supporting check: mean excess 5-bar return in the forecast's direction: 0.00412373, passed: True
- Counts: independent cases (grid days) in the choppy profile: 429, cases: 1641
- Decided by: The slope's t is between -2 and 2.
- Reading: Choppy profile read as the recorded regime 'unknown' (the only regime with a strategy) and the expected side as the sign of the raw swing-scaled return; normal drift is each coin's mean non-overlapping 5-bar return over all its windows; same-day cases are pooled by averaging their forecast and excess return, the slope t is the ordinary OLS t on those daily points, the supporting mean is over all cases, and the plan's under-100 grid-days rule is applied as 'not observable'.
- Size: unusual move +0.67 % (t 1.98, the cases of one day together: 1171 days) per case over 5 bars, 0.035 of the coin's usual move (12.35 %); normal drift in its direction -0.02 %, total +0.65 %; 2254 cases
Plan: `steps_cards/03_test_plan/night7_rangefail_run/plans/039-01_choppy-swing-scaled-weeks-rise-continues_1d.md`
Record: `steps_cards/04_backtest/night7_rangefail_run/backtests/039-01_choppy-swing-scaled-weeks-rise-continues_1d`
Measure: `measure.py`
