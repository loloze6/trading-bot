---
idea: 010-03_rsi-above-streak-continuation
brief: 010_rsi-midline-regime-direction
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
---
Fidelity:
- Situation: 14-day RSI above 50 without a break, counted in days up to the current close -> replaced: the catalogue has the RSI level, but no component counts how long it has stayed above 50.
- Comparison: longer unbroken stretches against shorter ones -> kept: the forecast would grow with the stretch length.
- Outcome: higher coin return over the next 14 days -> kept: 14 bars on daily bars.
- Verdict transfer: no: the RSI level or price momentum is a different quantity from the length of an RSI-above-50 run, so their result says nothing about the run length.
Reason: The run length of RSI(14) above 50 can be computed from the coin's own closes, and as a graded count the config could hold it. No catalogue component computes it, and no composition can: `RSIPullbackComponent` gives only RSI's level, `MovingAverageAgeComponent` counts runs of the close against an SMA rather than RSI against 50, and no transform op counts consecutive bars.
