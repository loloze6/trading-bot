---
idea: 016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift.d1_late-utc-rebound-after-falls
brief: 016_grind-versus-jump-moves
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: missing-components
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: in the 21:00–23:00 UTC slot, 7-day hourly volatility, amplified by the fall over the past 24 hours -> replaced: the slot and each measure can be built, but only as an additive mix of volatility and fall, not volatility made larger by the fall.
- Comparison: larger rise with higher volatility, the more so the further the coin fell -> replaced: a weighted sum cannot make the volatility effect grow with the fall.
- Outcome: price rises from 21:00 to 23:00 UTC (2 bars) -> kept
- Verdict transfer: no: an additive test could confirm or reject without the interaction that the idea depends on.
Reason: The forecast in the 21:00–23:00 slot must grow with 7-day volatility times the 24-hour fall. A config forecast is a weighted sum of components, and `score_product` only gates, it does not size. No catalogue component computes this product from closes: `VolatilityRankedFallComponent` uses a one-bar fall and a 120-bar volatility rank, not a 24-hour fall and 168-bar volatility.
