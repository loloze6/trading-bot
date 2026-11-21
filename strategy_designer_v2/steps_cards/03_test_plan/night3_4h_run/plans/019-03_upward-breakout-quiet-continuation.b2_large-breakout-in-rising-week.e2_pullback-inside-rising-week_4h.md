---
idea: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.e2_pullback-inside-rising-week
brief: 019_quiet-range-then-breakout-on-four-hour-bars
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 4h
data-period: folds A, B, C, D
outcome: missing-components
catalogue: 3d6ac1c822df
---
Fidelity:
- Situation: 7-day return positive, and the 4h close far below the prior two days' highest high, in 30-day average 4h ranges -> replaced: no catalogue component gives that depth in mean bar ranges; percent depth would replace it.
- Comparison: deeper pullbacks against shallower ones -> adapted: graded, so the position grows with the depth.
- Outcome: the coin rises over the next three days (18 bars) -> kept
- Verdict transfer: no: a test on percent depth, or on depth over its own past size, measures a different quantity than depth in 30-day mean ranges.
Reason: The 7-day condition can be built as a regime rule on PriceEvolutionComponent (period 42) above 0. The depth below the prior 12-bar high in units of the 180-bar mean bar range cannot be built: BreakoutInMeanRangesComponent gives only the break above that high, and no composition can divide DistanceFromHighComponent's percent depth by the mean bar range, because configs combine components only by weighted sums.
