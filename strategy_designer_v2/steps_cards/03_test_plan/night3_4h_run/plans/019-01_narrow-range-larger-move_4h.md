---
idea: 019-01_narrow-range-larger-move
brief: 019_quiet-range-then-breakout-on-four-hour-bars
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 4h
data-period: folds A, B, C, D
outcome: untestable
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: average 4h high-low range over the past two days, narrow against the past 30 days -> replaced: no component averages bar ranges; the nearest measure is the max-high minus min-low band (RangeCompressionRatio, 12 vs 180 bars) or the return-std ratio.
- Comparison: the two-day average range against the 30-day average range -> replaced: by a ratio of total bands or of return volatilities, not of average ranges.
- Outcome: a larger absolute return over the next three days (18 bars), either direction -> replaced: a position profits only when its side matches the move, so the size of a move cannot be bet on.
- Verdict transfer: no: a signed long or short book cannot earn or lose from the size of a move whatever its direction, so its result says nothing about the idea.
Reason: The idea predicts the size of the next three days' move, not its direction. A config's forecast is a signed position that gains only when its side matches the price's direction, and it cannot express a bet on the size of a move in either direction.
