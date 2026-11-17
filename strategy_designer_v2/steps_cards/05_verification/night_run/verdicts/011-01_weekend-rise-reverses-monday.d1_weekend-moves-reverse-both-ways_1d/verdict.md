---
plan: 011-01_weekend-rise-reverses-monday.d1_weekend-moves-reverse-both-ways_1d
idea: 011-01_weekend-rise-reverses-monday.d1_weekend-moves-reverse-both-ways
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of mean of (forecast/10) x 2-bar excess return on Sunday bars: 0.00428853; ordinary t of the mean: 2.75089 (threshold: mean > 0 with t >= 2 (confirm, with supporting check); mean < 0 with t <= -2 (reject))
- Supporting check: top-third minus bottom-third mean of sign(forecast) x excess, by |forecast|: -0.00234958, passed: False
- Counts: Sunday cases with a full 2-bar outcome: 2465, active bars: 2506
- Decided by: t >= 2 but the supporting check fails (top third by |forecast| does not beat the bottom third).
- Reading: Cases are Sunday bars (timestamp day of week = Sunday) with regime mean_reversion and a close two bars later in the same window, including any with forecast 0; the coin's mean 2-bar return is taken on the non-overlapping grid (positions 0,2,4,... of each window) pooled over all its windows; thirds are floor(n/3) cases at each end after sorting by |forecast|.
Plan: `steps_cards/03_test_plan/night_run/plans/011-01_weekend-rise-reverses-monday.d1_weekend-moves-reverse-both-ways_1d.md`
Record: `steps_cards/04_backtest/night_run/backtests/011-01_weekend-rise-reverses-monday.d1_weekend-moves-reverse-both-ways_1d`
Measure: `measure.py`
