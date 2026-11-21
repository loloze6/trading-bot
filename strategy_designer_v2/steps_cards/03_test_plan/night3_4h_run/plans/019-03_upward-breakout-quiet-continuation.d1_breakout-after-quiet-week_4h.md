---
idea: 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week
brief: 019_quiet-range-then-breakout-on-four-hour-bars
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 4h
data-period: folds A, B, C, D
outcome: missing-components
catalogue: ad5059559106
---
Fidelity:
- Situation: a 4h close above the highest high of the preceding two-day (12-bar) stretch, larger the narrower that stretch is against the 30-day (180-bar) average 4h range -> adapted: the breakout threshold becomes graded by `NarrowRangeBreakoutComponent` (period 12, base_period 180), whose value grows with the breakout's size times B/S.
- Comparison: the coin's average 4h range over the past 7 days (42 bars) against its average over the past 60 days (360 bars), with the breakout's weight growing as that ratio falls -> replaced: no component averages high minus low over two windows, and the config cannot multiply the breakout by such a ratio.
- Outcome: the coin rises over the next three days (18 bars) -> kept: the book holds each bet for 18 bars, long only.
- Verdict transfer: no: without the quiet-week weighting, a result would test only the plain narrow-range breakout, not this idea.
Reason: The bars hold everything the idea needs, but no component computes the 7-day over 60-day average 4h range ratio. The config's weighted mean cannot multiply it into the breakout either: adding it would open positions with no breakout, and a regime would make it on/off. A single graded component computing the product, as `NarrowRangeBreakoutComponent` already combines its own two factors, would hold the idea.
