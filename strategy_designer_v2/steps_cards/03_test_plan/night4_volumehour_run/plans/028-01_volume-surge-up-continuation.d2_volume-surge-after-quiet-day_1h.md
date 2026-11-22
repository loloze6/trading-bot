---
idea: 028-01_volume-surge-up-continuation.d2_volume-surge-after-quiet-day
brief: 028_volume-confirmed-hourly-moves-continue
data-instruments: BTC, ETH
data-bar: 1h
data-period: folds A, B, C, D
outcome: missing-components
catalogue: 6e9b10174437
---
Fidelity:
- Situation: an hour rising far more than its typical 30-day hourly move, on volume several times its 30-day average -> adapted: graded as the hour's return in 720-bar standard deviations times its volume over the 720-bar mean (VolumeWeightedScaledReturnComponent, clipped to up-hours).
- Comparison: the coin's 24-hour return before that hour; modest allows the rise, larger weakens it, the largest turns it into a fall -> replaced: no catalogue component multiplies the shock by the prior 24-hour rise, and a weighted sum would hold positions with no shock.
- Outcome: price keeps rising over the next 2 to 6 hours (up after modest prior rises, down after the largest) -> kept: a 6-bar horizon on 1h bars.
- Verdict transfer: no: without the shock-times-prior-rise interaction, the test cannot show the further rise weakening and reversing as the prior 24-hour rise grows, which is the idea's own claim.
Reason: The idea needs a product of the volume-confirmed up-hour shock with the coin's prior 24-hour return. Regimes would only turn that graded weakening into steps, a weighted sum takes positions on hours with no shock, and the weighted mean cancels any per-regime weight scaling. All the inputs are in one coin's closes and volumes, so a product component would let a config written as shock minus shock times prior rise express the idea.
