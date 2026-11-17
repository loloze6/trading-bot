---
idea: 012-04_flush-depth-retracement-size
brief: 012_liquidation-flush-partial-rebound
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
---
Fidelity:
- Situation: a bar that falls sharply, on a volume burst, with a long lower wick -> replaced: no catalogue component reads the bar's low against its open or close, so the wick can only be swapped for close-to-close falls.
- Comparison: a larger drop from the bar's open to its low, among such bars -> replaced: no component computes the open-to-low drop, and only close-based fall sizes exist.
- Outcome: price rises over the next 3 days, back toward its pre-cascade level -> kept: the forward return over 3 bars on daily bars.
- Verdict transfer: no: without the wick and the open-to-low depth, the test would measure ordinary heavy-volume closing falls, not liquidation flushes.
Reason: Two parts of the idea need intrabar shape: the long lower wick and the bar's drop from open to low. No catalogue component computes either, alone or combined. These come from the coin's own open, high, low and close columns. The config could hold them: a regime rule on the wick, together with `VolumeRatioComponent` and a sharp fall from `VolatilityScaledReturnComponent`, plus a graded component on the open-to-low depth.
