---
plan: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.g2_weekend-rise-fades-early-week_1d
idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.g2_weekend-rise-fades-early-week
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: |forecast|-weighted mean 3-day shortfall vs coin drift (short direction), before costs: 0.00915733; t of the weighted mean: 3.56232 (threshold: confirm: mean > 0 with t >= 2 and correlation > 0; reject: mean < 0 with t <= -2)
- Supporting check: Pearson correlation of |forecast| with shortfall: -0.00106492, passed: False
- Counts: cases (Sunday rises): 2559
- Decided by: t >= 2 but the correlation is 0 or below (or undefined), so the plan's inconclusive rule applies.
- Reading: A Sunday bar is a bar whose UTC start timestamp is a Sunday (its close is the Sunday close, the next bar Monday), the raw rise uses last_history_value (recomputed from prices where missing), cases are Sunday bars with forecast < 0 and 3 bars left in the window, the coin's drift is the mean of its non-overlapping 3-bar returns pooled over all its windows, and the t of the |forecast|-weighted mean uses the weighted standard error sqrt(n/(n-1) * sum(w^2 (x-m)^2)) / sum(w).
- Size: unusual move +0.98 % per case over 3 bars, 0.108 of the coin's usual move (9.14 %); normal drift in its direction -0.47 %, total +0.51 %; 2157 cases
Plan: `steps_cards/03_test_plan/retest_monday_run/plans/011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.g2_weekend-rise-fades-early-week_1d.md`
Record: `steps_cards/04_backtest/retest_monday_run/backtests/011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.g2_weekend-rise-fades-early-week_1d`
Measure: `measure.py`
