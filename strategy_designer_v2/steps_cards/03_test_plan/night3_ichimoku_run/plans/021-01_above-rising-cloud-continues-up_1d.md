---
idea: 021-01_above-rising-cloud-continues-up
brief: 021_ichimoku-cloud-as-a-watched-equilibrium
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: close above the Ichimoku cloud and the cloud rising -> replaced: no component computes the displaced high-low-midpoint cloud or its rise.
- Comparison: larger return the faster the cloud rose over the past 26 days -> replaced: no component computes the cloud's 26-day rate of rise.
- Outcome: positive return over the next 26 days -> kept: held 26 bars on daily bars.
- Verdict transfer: no: stand-ins such as Donchian position or moving-average slope measure a different object, and the brief asks whether the cloud adds anything beyond those.
Reason: The cloud is built from 9-, 26- and 52-bar high-low midpoints displaced 26 bars forward, all from the coin's own high and low columns, and the config could hold it as a regime plus a graded component. No catalogue component computes high-low midpoints with a displacement, alone or in combination: `DistanceFromHighComponent` gives only the distance to one extreme, and there is no lag op.
