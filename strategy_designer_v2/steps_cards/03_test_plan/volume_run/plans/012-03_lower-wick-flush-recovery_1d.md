---
idea: 012-03_lower-wick-flush-recovery
brief: 012_liquidation-flush-partial-rebound
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
---
Fidelity:
- Situation: a bar that falls sharply on a volume burst -> adapted: a regime that is active while VolatilityScaledReturn(1, 20) is a large fall and VolumeRatio(30) is a burst.
- Comparison: a longer lower wick below the close, as a share of the bar's high-to-low range -> replaced: no catalogue component measures the bar's low against its close and its range.
- Outcome: a larger price rise over the next 3 days -> kept: the 3-bar forward return on 1d bars, long.
- Verdict transfer: no: without the wick share, a test cannot show whether a longer wick brings a larger rebound.
Reason: The idea's graded variable is the lower wick as a share of the bar's range, (close - low) / (high - low). Only the coin's own high, low and close are needed, and the config could hold it as a graded forecast inside a fall-on-volume regime. No component computes it, and no combination of components does either. Only ADXDirectional and KeltnerBreakout read high and low, and both smooth them over many bars; neither measures the current bar's low against its close.
