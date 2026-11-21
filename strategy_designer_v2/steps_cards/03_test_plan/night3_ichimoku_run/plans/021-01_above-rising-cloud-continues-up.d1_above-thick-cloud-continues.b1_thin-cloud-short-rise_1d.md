---
idea: 021-01_above-rising-cloud-continues-up.d1_above-thick-cloud-continues.b1_thin-cloud-short-rise
brief: 021_ichimoku-cloud-as-a-watched-equilibrium
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: a31b77de3651
---
Fidelity:
- Situation: close above the Ichimoku cloud while the cloud rises -> kept: a regime rule on IchimokuCloudPositionComponent > 0 and IchimokuCloudSlopeComponent > 0.
- Comparison: a thinner cloud (span gap as a share of price) gives a larger return -> replaced: no positive reading that grows as the cloud thins exists without a constant offset, and the guide forbids a constant inside a regime.
- Outcome: the return over the next 5 days is larger, long side -> kept: 5 bars on daily bars, long only.
- Verdict transfer: no: the only usable thinness readings either go short on thick clouds (negated width) or mix in another quantity, so a result would not judge the idea's own relation.
Reason: The situation is a regime the detector can express. Inside it the forecast must be long and grow as the cloud thins. IchimokuCloudWidthComponent only grows with thickness, and negating it makes it always negative (short). Centring it needs a BuyAndHoldStrategy offset, which the guide forbids inside a regime. Mixing in another positive component, such as the distance above the cloud, replaces the comparison.
