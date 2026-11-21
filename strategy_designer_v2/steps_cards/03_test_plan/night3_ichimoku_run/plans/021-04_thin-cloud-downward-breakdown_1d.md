---
idea: 021-04_thin-cloud-downward-breakdown
brief: 021_ichimoku-cloud-as-a-watched-equilibrium
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: a daily close crossing from above the Ichimoku cloud to below it -> replaced: no catalogue component computes the cloud (spans from 9/26/52-bar high-low midpoints, displaced 26 bars), so only a Donchian or moving-average proxy could be used.
- Comparison: the cloud's width relative to price at the cross, thinner meaning a larger fall -> replaced: no component computes the gap between the two displaced spans over the close.
- Outcome: the coin falls over the next 26 days -> kept: a 26-bar horizon on daily bars.
- Verdict transfer: no: a proxy for the cloud is the plain trend the brief must be told apart from, so neither result would bear on the cloud itself.
Reason: The cloud is computed from the coin's own high and low and could be held as a graded component. No catalogue component, alone or combined, gives the 26-bar-displaced midpoint spans or their width. DistanceFromHighComponent and DonchianBreakoutComponent have no displacement, and no transform shifts a value back in time.
