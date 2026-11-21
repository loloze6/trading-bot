---
idea: 019-02_narrow-range-wider-span
brief: 019_quiet-range-then-breakout-on-four-hour-bars
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 4h
data-period: folds A, B, C, D
outcome: untestable
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: the coin's average 4h high-low range over the past two days (12 bars) is narrow -> replaced: no catalogue component averages bar ranges; RangeCompressionRatioComponent measures the total span of the window instead.
- Comparison: against its average 4h range over the past 30 days (180 bars) -> replaced: the same span ratio, not a ratio of average ranges.
- Outcome: a wider highest-high-to-lowest-low span over the next three days (18 bars), relative to price, with no direction -> replaced: a forecast can only take a long or short position, which pays on net direction, not on span.
- Verdict transfer: no: a directional book cannot confirm or reject a claim about the size of the price span with no direction.
Reason: The idea predicts how wide the coming three-day span is, regardless of direction. A config can only hold a signed position, which earns from the net direction of the price, so no forecast can bet on the span. The situation would also need an average-bar-range component that is not in the catalogue, but the direction-free outcome alone puts the idea outside the config's logic.
