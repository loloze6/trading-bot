---
idea: 019-04_downward-breakout-quiet-continuation
brief: 019_quiet-range-then-breakout-on-four-hour-bars
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 4h
data-period: folds A, B, C, D
outcome: missing-components
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: a 4h bar closes below the lowest low of the preceding two-day (12-bar) stretch -> adapted: a regime veto on `DistanceFromHighComponent` (period 12, source "high", extreme "low", exclude_current 1) below 0 makes "after the break" into "while the close is below that low".
- Comparison: that stretch's narrowness against the coin's 30-day (180-bar) average four-hour range -> replaced: the catalogue only offers `RangeCompressionRatioComponent`, which divides by the whole 30-day span, not by the average bar range.
- Outcome: the coin falls over the next three days (18 bars), more the narrower the stretch was -> kept: a graded short sized by narrowness, held 18 bars.
- Verdict transfer: no: sizing by the share of the 30-day span tests a different narrowness, so its result would not confirm or reject this idea.
Reason: The narrowness of the 12-bar stretch must be compared with the average 4h bar range (mean of high minus low) over 180 bars, and no catalogue component computes that. `RangeCompressionRatioComponent` divides by the 30-day high-low span, `VolatilityRatioToAverageComponent` uses close-to-close return volatility, and no ATR or average-range output exists to combine with the others.
