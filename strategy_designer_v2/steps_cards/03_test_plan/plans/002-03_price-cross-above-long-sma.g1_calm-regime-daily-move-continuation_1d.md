---
idea: 002-03_price-cross-above-long-sma.g1_calm-regime-daily-move-continuation
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
---
Fidelity:
- Situation: in a coin whose 20-day volatility of daily returns is low, one day's return is large relative to that volatility -> replaced: no catalogue component divides a day's return by the 20-day standard deviation of returns. `vol_normalize` divides by the 24-bar standard deviation of price levels times the close, which is a different quantity.
- Comparison: a stronger effect at low 20-day volatility, weaker or reversed as volatility rises -> adapted: the low-volatility condition becomes a regime on the 20-bar `VolatilityPercentileRegimeComponent`.
- Outcome: price moves the same way as that day over the next 5 days, more for larger scaled moves -> kept: a signed position over a 5-bar horizon, sized by the scaled move.
- Verdict transfer: no: a test on return over price-level dispersion, or on distance from an EMA in ATR units, could confirm or reject that proxy without testing the idea's volatility-scaled daily return.
Reason: The idea's situation is one day's return divided by the 20-day standard deviation of daily returns. The config can only add components by weight, and no component computes that ratio. `vol_normalize` uses the standard deviation of price levels and adds a close-squared scale. `KeltnerBreakoutComponent` measures distance from an EMA in true-range units. Neither is the scaled daily return.
