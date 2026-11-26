---
idea: 076-01_agitated-wide-high-close-fades
brief: 076_agitated-wide-high-close-fade
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: 607e0219f5c3
---
Fidelity:
- Situation: agitated day, range wide vs 20-day average range, close near its high, the two multiplying -> replaced: no catalogue component gives their product, and a weighted mean only adds them.
- Comparison: day's range against the coin's average range over the past 20 days -> kept: `RangeCompressionRatioComponent` (short 1, long 20, `base` "mean_bar_range", `form` "width") measures it, but only as a regime measure.
- Outcome: price falls over the next day, more for wider, higher-closing days -> kept: a short over a 1-bar horizon on 1d bars.
- Verdict transfer: no: a sum of close location and range multiple is large on a high close on an ordinary-width day, which the idea says gives little fall.
Reason: The forecast must be graded by the product of the day's range multiple and its close location. That product equals (close[t] − low[t]) / mean(high − low over the last 20 bars). The config can only take weighted means of components, and no catalogue component computes this product: `RiseTimesRangeMultipleComponent` uses the close-to-close rise, `VolumeWeightedCloseLocationComponent` uses volume, and `DistanceFromHighComponent` (`extreme` "low") is in percent of the low, not in mean bar ranges.
