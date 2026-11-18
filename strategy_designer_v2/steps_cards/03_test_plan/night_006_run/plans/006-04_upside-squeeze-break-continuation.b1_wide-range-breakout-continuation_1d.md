---
idea: 006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation
brief: 006_range-compression-precedes-expansion
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: 70a362722b07
---
Fidelity:
- Situation: a coin closes above the high of its prior 20 days -> kept: a regime rule on DistanceFromHighComponent (period 20, source high, exclude_current 1) above 0.
- Comparison: the wider the 20-day range against the 100-day range -> replaced: RangeCompressionRatioComponent grows as the range narrows, and a constant offset cannot flip it inside a regime.
- Outcome: price rises further over the next 10 days -> kept: a long position, judged over 10 daily bars.
- Verdict transfer: no: no catalogue component grades the long position upward with the range's width inside the breakout regime, so a result would not bear on the idea.
Reason: The breakout can be a regime, and its position must grow with the 20-day range's share of the 100-day range. The only range measure, RangeCompressionRatioComponent, falls as that share rises. Turning it around needs a constant offset (+10 minus the standardised compression), and a constant is not allowed inside a regime. No other component computes the range ratio.
