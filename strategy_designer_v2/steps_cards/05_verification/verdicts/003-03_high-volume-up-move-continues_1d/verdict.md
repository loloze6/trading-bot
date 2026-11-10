---
plan: 003-03_high-volume-up-move-continues_1d
idea: 003-03_high-volume-up-move-continues
fit: adapted
status: rejected
---
Evidence:
- Main measure: position-weighted mean next-bar excess return on active bars: -0.000694036; t of the weighted mean: -0.248811 (threshold: above 0 with t >= 2 to confirm; <= 0 rejects)
- Supporting check: top-third minus bottom-third positions, mean next-bar return: -0.000546063, passed: False
- Counts: active bars: 151
- Decided by: The position-weighted mean next-bar excess return is <= 0, which meets the reject rule.
- Reading: Position is postRebalance_current_allocation; excess is each active bar's next-bar return minus the mean next-bar return of all bars in its own window; the t of the weighted mean uses the weighted standard error sqrt(sum w^2 (x-m)^2)/sum w times sqrt(n/(n-1)); the thirds are the n//3 largest and n//3 smallest positions among pooled active bars (ties broken by order), compared on unweighted raw next-bar returns with Welch t.
Plan: `steps_cards/03_test_plan/plans/003-03_high-volume-up-move-continues_1d.md`
Record: `steps_cards/04_backtest/backtests/003-03_high-volume-up-move-continues_1d`
Measure: `measure.py`
