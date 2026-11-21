---
idea: 021-02_below-falling-cloud-continues-down
brief: 021_ichimoku-cloud-as-a-watched-equilibrium
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: coin closes below its Ichimoku cloud while the cloud is falling -> replaced: no catalogue component computes the cloud, so only a moving-average or close-range proxy is possible.
- Comparison: the faster the cloud has fallen over the past 26 days, the more negative the return -> replaced: no component measures the cloud's 26-day change, only a moving-average slope.
- Outcome: return over the next 26 days is negative -> kept: a 26-bar horizon, short side.
- Verdict transfer: no: a moving-average proxy would test a plain trend, which the brief names as the baseline the cloud must beat.
Reason: The Ichimoku cloud is two midpoints of high-low ranges (9/26 and 52 bars), plotted 26 bars ahead, and all of it comes from the coin's own bars. No catalogue component computes these midpoints, displaces them, or measures the cloud's slope. Combining DistanceFromHighComponent "high" and "low" does not give the range midpoint, because the two use different denominators, and no component has the 26-bar displacement.
