---
idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.g1_weekend-day-one-day-reversal.g1_high-volume-weekend-moves-reverse
brief: 011_weekend-moves-reverse-weekday
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
---
Fidelity:
- Situation: a Saturday or Sunday one-day move, scaled by its 20-day volatility -> kept: a weekday regime rule plus VolatilityScaledReturnComponent(period 1, vol_period 20).
- Comparison: the reversal grows with that day's volume relative to its 20-day usual volume -> replaced: no catalogue component reads volume as a graded value, so only an on/off volume gate or nothing at all could stand in.
- Outcome: the move reverses over the next day -> kept: the negated forecast, judged on the 1-bar forward return.
- Verdict transfer: no: without the volume weighting, the test checks a plain weekend fade, not the idea's volume-graded reversal.
Reason: The idea's size must be the volatility-scaled weekend move times that day's volume over its 20-day average volume. The catalogue has no graded relative-volume component. The only volume tools (VolumeExpansionHedgeComponent, volume_filter) are on/off, and a regime's weighted mean of components cannot form the product.
