---
idea: 012-01_liquidation-flush-rebound
brief: 012_liquidation-flush-partial-rebound
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
---
Fidelity:
- Situation: a bar closes sharply lower on far-above-average volume with a long lower wick -> replaced: the sharp fall fits VolatilityScaledReturnComponent, but no component measures volume or the lower wick.
- Comparison: volume against its own 30-day average volume, and the wick below the close -> replaced: no component computes either quantity, alone or combined.
- Outcome: price rises over the next 3 days, more after bigger bursts and longer wicks -> kept: a 3-bar horizon on daily bars.
- Verdict transfer: no: without the volume burst and the wick, the test measures only sharp falls, which the brief says is not this idea.
Reason: The volume burst and the lower wick both come from the coin's own bars (volume, open, low, close), and a graded strategy component could carry them. No catalogue component computes them: volume_filter is an on/off dead zone at average volume, VolumeExpansionHedgeComponent fires only on low-volume up bars, and nothing reads the bar's low against its close.
