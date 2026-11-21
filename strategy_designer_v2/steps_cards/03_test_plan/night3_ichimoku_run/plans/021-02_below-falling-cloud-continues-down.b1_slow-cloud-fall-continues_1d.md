---
idea: 021-02_below-falling-cloud-continues-down.b1_slow-cloud-fall-continues
brief: 021_ichimoku-cloud-as-a-watched-equilibrium
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: a31b77de3651
---
Fidelity:
- Situation: the coin closes below its Ichimoku cloud and the cloud is falling -> kept: a regime rule on `IchimokuCloudPositionComponent` (edge "nearest") < 0 and `IchimokuCloudSlopeComponent` (lookback 26) < 0.
- Comparison: more negative the more slowly the cloud has fallen over the past 26 days -> replaced: no catalogue measure grows as the fall slows, so only a barred constant offset could grade it.
- Outcome: negative return over the next 26 days -> kept: a short held for 26 bars on daily bars.
- Verdict transfer: no: without a size that grows as the cloud's fall slows, the test cannot check the idea's gradient or its "refuse the short after a fast collapse".
Reason: The gradient needs a short that is largest when the cloud's slope is near zero and shrinks as the fall speeds up. `standardise`, `negate`, `clip` and `signed_power` all give 0 at slope 0. `sigmoid` stays within ±0.5, below the 2-point trading band, and no scale op is allowed after `standardise`. A constant offset inside the regime is barred, and the other cloud measures (position, width) are different quantities.
