---
idea: 016-04_down-jump-price-reversal.g1_volatile-regime-daily-move-reversal
brief: 016_grind-versus-jump-moves
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: missing-components
catalogue: 1f000a7ba652
---
Fidelity:
- Situation: a large 24-hour return measured in units of the past 7-day hourly volatility -> kept: `VolatilityScaledReturnComponent` with period 24 and vol_period 168.
- Comparison: the reversal is stronger the higher the 7-day volatility stands against its own usual level -> replaced: a weighted sum cannot make the fade's size grow with the volatility ratio, so the interaction cannot be built.
- Outcome: price moves the opposite way over the next 24 hours -> kept: `negate` after `standardise`, horizon 24 bars.
- Verdict transfer: no: without the volatility-ratio interaction, a test of the plain fade would not confirm or reject the idea's claim that the reversal grows with relative volatility.
Reason: The idea needs a product: the volatility-scaled 24-hour move times the 7-day volatility's ratio to its usual level. The config only forms weighted sums of components. A regime on the volatility ratio would be on/off, not graded in the ratio. No catalogue component carries this product: `RankWeightedScaledMoveComponent` weights the move the opposite way (less when volatility ranks high), and `VolatilityRankedFallComponent` uses one bar and falls only.
