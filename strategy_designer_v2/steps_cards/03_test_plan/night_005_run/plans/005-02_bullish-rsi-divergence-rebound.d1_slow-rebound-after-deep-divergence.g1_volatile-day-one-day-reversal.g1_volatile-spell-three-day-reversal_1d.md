---
idea: 005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence.g1_volatile-day-one-day-reversal.g1_volatile-spell-three-day-reversal
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 4e6cc97f57e5
---
Fidelity:
- Situation: 20-day volatility high relative to its 60-day average -> adapted: the condition is a regime that is active while the 20-day volatility is at or above its 60-day mean (ratio 1.0, by convention).
- Comparison: the day's return against its 20-day volatility, scaled up by the volatility ratio -> kept: (r / s20) x (s20 / mean s) = r / (60-day average volatility), which is the 1-day return divided by its own 60-day mean absolute size.
- Outcome: return over the next 3 days runs against the day just closed, and is larger for larger readings -> adapted: the 3-day holding period is dropped, and the forecast is recomputed on each bar.
- Verdict transfer: yes: the forecast is the idea's graded reading on its own condition, and the 3-bar outcome is measured as the idea states it.
Forecast: The forecast is computed only on bars where VolatilityRatioToAverageComponent (vol_period 20, vol_lookback 60) is at least 1.0. On all other bars it is 0 (flat). On active bars it is minus the day's percent return (PriceEvolutionComponent, period 1), standardised against the mean absolute daily return of the previous 60 bars (min 20), times 10, capped at ±20. The sign is negative after an up day and positive after a down day. Its size grows with the day's move against the coin's 60-day average volatility. That size equals the move in 20-day usual moves times the volatility ratio, so it grows with both.
Config: 005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence.g1_volatile-day-one-day-reversal.g1_volatile-spell-three-day-reversal_1d_config.json
Criterion:
- Horizon: 3 bars
- Main measure: Use the non-overlapping grid of bars 0, 3, 6, ... of each window, keeping only bars whose regime is mean_reversion. For each kept bar, multiply forecast/10 by (the coin's 3-bar forward return minus the coin's mean 3-bar return over all windows). Take the t of the mean of that product, pooled over coins and windows.
- Supporting check: On the same cases, the mean product in the top third of |forecast| minus the mean product in the bottom third is above 0.
- Confirm: The main measure's t is at least +2 and the supporting check passes.
- Reject: The main measure's t is at most -2.
- Inconclusive: Any t between -2 and +2 is inconclusive. A t of at least +2 with a failed supporting check is also inconclusive. At least 100 grid cases pooled are required, or the result is inconclusive.
