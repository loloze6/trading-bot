---
plan: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins_1d
idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of mean of x = (-forecast/10) * -(r2 - coin mean 2-bar return), Sunday short cases: 0.0084513; ordinary t of the mean: 4.87648 (threshold: confirm t >= 2 with check < 0; reject t <= -2; at least 100 cases)
- Supporting check: mean(r2 - m) top third minus bottom third by |forecast|: 0.00286097, passed: False
- Counts: cases: 2574
- Decided by: t >= 2 but the supporting check is at or above 0, which the plan rules inconclusive.
- Reading: Sunday bar = bar whose UTC start is a Sunday (next bar Monday); 'rose' read as raw 1-bar return > 0; cases need t+2 inside the window; thirds by |forecast| from a stable ascending sort split with np.array_split; fewer than 100 cases reported as not observable per the minimum-count rule.
Plan: `steps_cards/03_test_plan/night_run/plans/011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins_1d.md`
Record: `steps_cards/04_backtest/night_run/backtests/011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins_1d`
Measure: `measure.py`
