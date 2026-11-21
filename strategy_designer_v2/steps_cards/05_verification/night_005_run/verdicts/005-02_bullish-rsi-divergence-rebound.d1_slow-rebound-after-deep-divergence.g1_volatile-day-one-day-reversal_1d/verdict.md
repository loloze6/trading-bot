---
plan: 005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence.g1_volatile-day-one-day-reversal_1d
idea: 005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence.g1_volatile-day-one-day-reversal
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope of next-bar excess return on forecast/10 (high-vol bars): 0.00303011; OLS t of pooled slope: 3.66311 (threshold: confirm: slope > 0 with t >= 2 and >= 2 of 3 coins positive; reject: slope < 0 with t <= -2 and >= 2 of 3 coins negative)
- Supporting check: coins with per-coin slope of pooled sign (need >= 2): 2, passed: True
- Counts: pooled high-volatility bars: 2571, high-volatility bars BTCUSD: 1238, high-volatility bars ETHUSD: 1333
- Decided by: Pooled slope positive with t >= 2 and at least 2 coins with positive slopes.
- Reading: The situation is rebuilt in each window as the 20-day std of daily returns at or above its 60-bar mean (falling back on regime == 'trending' where the window is too short to rebuild it), the expected side is opposite to the day's scaled move; the OLS includes an intercept; the per-coin minimum of 60 and the '2 of the 3 coins' rule are applied to the coins present in the record.
- Size: unusual move +0.33 % per case over 1 bars, 0.085 of the coin's usual move (4.01 %); normal drift in its direction -0.00 %, total +0.33 %; 1697 cases
Plan: `steps_cards/03_test_plan/night_005_run/plans/005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence.g1_volatile-day-one-day-reversal_1d.md`
Record: `steps_cards/04_backtest/night_005_run/backtests/005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence.g1_volatile-day-one-day-reversal_1d`
Measure: `measure.py`
