---
idea: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d1_trend-conditioned-one-day-reversal
brief: 005_rsi-divergence-predicts-reversal
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: a 1-day fall (or rise) large relative to its own 20-day daily volatility -> kept: `VolatilityScaledReturnComponent` (period 1, vol_period 20).
- Comparison: the 50-day return sets the size; the fade applies only while it is negative -> replaced: the catalogue can only add the 50-day return to the move, not multiply it in.
- Outcome: the coin rises after the fall, or gives back after the rise, over the next 1 day -> kept: a 1-bar horizon.
- Verdict transfer: no: an additive mix bets on the 50-day trend even with no outsized day, so its result would not judge the idea's interaction.
Reason: The idea's size is the vol-scaled 1-day move times the 50-day return. A regime on the 50-day return's sign can hold the "only while negative" part. But no component multiplies the vol-scaled move by the 50-day return. `MomentumDivergenceComponent` (periods 2 and 51) gives the raw 1-day return times the 50-day return. That replaces the 20-day vol scaling, and `vol_normalize` divides by the price-level stddev_24, not by return volatility.
