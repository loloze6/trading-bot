---
idea: 021-03_thin-cloud-upward-breakout
brief: 021_ichimoku-cloud-as-a-watched-equilibrium
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: a daily close crossing up from below the Ichimoku cloud to above it -> replaced: no component computes the 26-bar-displaced spans of high/low midpoints, so only a different quantity could stand in.
- Comparison: the cloud's width relative to price at the cross, thinner meaning larger rise -> replaced: no component computes the gap between the two cloud spans.
- Outcome: the coin rises over the next 26 days -> kept: 26 bars on daily bars.
- Verdict transfer: no: a proxy such as a moving-average or Donchian position is the "plain trend" the brief must beat, so its verdict would say nothing about the cloud.
Reason: The cloud is built from the coin's own high and low, so the config could hold the idea. But no catalogue component computes high/low midpoints over 9, 26 and 52 bars, displaced 26 bars forward. DonchianBreakoutComponent reads closes and gives a range position, not a midpoint, and DistanceFromHighComponent gives one extreme, with no displacement. No weighted combination of those percent distances gives the cloud's spans or its width.
