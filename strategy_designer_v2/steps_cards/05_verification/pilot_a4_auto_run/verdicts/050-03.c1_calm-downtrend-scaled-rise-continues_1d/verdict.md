---
plan: 050-03.c1_calm-downtrend-scaled-rise-continues_1d
idea: 050-03.c1_calm-downtrend-scaled-rise-continues
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 7-bar excess return of forecast>0 cases over the coin's mean 7-bar return: 0.0208186; t of the mean, cases of one day pooled (day-clustered): 1.697 (threshold: confirm: mean > 0 with t >= 2 and slope > 0; reject: t <= -2; else inconclusive)
- Supporting check: OLS slope of 7-bar excess return on forecast: 0.00147677, passed: True
- Counts: independent cases (days): 78, cases: 148
- Decided by: The t lies between -2 and 2, which the plan calls inconclusive.
- Reading: Cases are grid bars (positions 0,7,14,... of each window, with a full 7-bar forward return inside it) with forecast > 0; the coin's mean 7-bar return is taken on the same grid over all its windows; the t sums each day's case deviations into one (day-clustered standard error); the plan's 'fewer than 30 days' rule is applied as the minimum count, giving 'not observable'.
- Size: unusual move +1.96 % (t 2.45, the cases of one day together: 192 days) per case over 7 bars, 0.146 of the coin's usual move (12.44 %); normal drift in its direction +0.52 %, total +2.47 %; 267 cases
- Effect check (common/verdicts.md): unclear: t in the idea's direction +1.697 (not below 1), 78 cases (30 needed)
Plan: `steps_cards/03_test_plan/pilot_a4_auto_run/plans/050-03.c1_calm-downtrend-scaled-rise-continues_1d.md`
Record: `steps_cards/04_backtest/pilot_a4_auto_run/backtests/050-03.c1_calm-downtrend-scaled-rise-continues_1d`
Measure: `measure.py`
