---
idea: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week
brief: 019_quiet-range-then-breakout-on-four-hour-bars
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 4h
data-period: folds A, B, C, D
outcome: missing-components
catalogue: ad5059559106
---
Fidelity:
- Situation: a 4h close above the highest high of the preceding two days (12 bars), only while the 7-day (42-bar) return is positive -> adapted: the break becomes graded, max(0, close − prior 12-bar high), and the positive 7-day return becomes a regime rule on PriceEvolutionComponent(42).
- Comparison: the distance above the two-day high, measured in the coin's 30-day (180-bar) average 4h range -> replaced: no component or composition divides the break by the mean bar range; the closest are a percent break or NarrowRangeBreakout's break × mean range / stretch range.
- Outcome: the coin rises over the next three days (18 bars), more for a larger break -> kept.
- Verdict transfer: no: a percent break, or one rescaled by the stretch's own width, is a different quantity from a break in average ranges, so neither result would carry to the idea.
Reason: The break size in units of the 30-day average 4h range can be built from the coin's own high, low and close bars, but no catalogue component outputs it. A strategy forecast is only a weighted mean of components, with no division of one by another. NarrowRangeBreakoutComponent multiplies the percent break by mean range / stretch range, and vol_normalize divides by the 24-bar standard deviation of the close, so both are replacements.
