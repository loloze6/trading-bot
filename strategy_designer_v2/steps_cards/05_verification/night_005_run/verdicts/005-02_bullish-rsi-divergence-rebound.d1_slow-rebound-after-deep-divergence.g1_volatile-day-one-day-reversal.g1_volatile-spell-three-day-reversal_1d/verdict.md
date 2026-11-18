---
plan: 005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence.g1_volatile-day-one-day-reversal.g1_volatile-spell-three-day-reversal_1d
idea: 005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence.g1_volatile-day-one-day-reversal.g1_volatile-spell-three-day-reversal
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of forecast/10 x (3-bar forward return minus coin mean), mean_reversion grid bars: 0.0101492; t of the mean: 3.32376 (threshold: t >= +2 confirms (with supporting check), t <= -2 rejects)
- Supporting check: mean product top third of |forecast| minus bottom third: 0.0256019, passed: True
- Counts: grid cases pooled: 849, active bars: 2583
- Decided by: The main measure's t is at least +2 and the top-minus-bottom third check is above 0.
- Reading: The coin's mean 3-bar return is taken over all grid bars of all its windows, the grid bars whose 3-bar forward return leaves the window are dropped, the thirds are the N//3 smallest and N//3 largest |forecast| cases after a stable sort, and the 100-case minimum is applied as 'not observable'.
Plan: `steps_cards/03_test_plan/night_005_run/plans/005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence.g1_volatile-day-one-day-reversal.g1_volatile-spell-three-day-reversal_1d.md`
Record: `steps_cards/04_backtest/night_005_run/backtests/005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence.g1_volatile-day-one-day-reversal.g1_volatile-spell-three-day-reversal_1d`
Measure: `measure.py`
