---
idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d1_nearness-power-reversal-long.d1_nearness-reversal-in-uptrends
brief: 022_weak-effects-combined-by-what-worked-before
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: edf20a924da4
---
Fidelity:
- Situation: the excess of nearness-to-90-day-high predictive power over its usual level, times today's nearness deviation -> kept: `ExcessPredictivePowerZComponent` (signal "high", 90, 365, 5).
- Comparison: the reading points against a past relation that implies a fall -> kept: `negate` makes the reading positive when power times deviation implies a fall, and `clip` keeps the long side.
- Outcome: the coin rises over the next 5 days, more the further price stands above its 100-day mean -> replaced: a weighted mean only adds the two readings, and a regime turns the graded scaling into on/off.
- Verdict transfer: no: neither the sum nor the gate tests a rise that grows with the product of the reversal reading and the uptrend.
Reason: The idea scales the long reversal reading by the distance above the 100-day mean. That is a product of two graded measures, and the config can only average components, so it cannot compute it. Both factors come from the coin's own closes, so a single component could hold the product.
