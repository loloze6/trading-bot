---
idea: 019-03_upward-breakout-quiet-continuation
brief: 019_quiet-range-then-breakout-on-four-hour-bars
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 4h
data-period: folds A, B, C, D
outcome: missing-components
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: a 4h bar closes above the highest high of the preceding two-day (12-bar) stretch -> adapted: graded as the close's percent distance above the prior 12-bar high (`DistanceFromHighComponent`, source high, exclude_current 1), clipped at 0.
- Comparison: how narrow that 12-bar stretch was against the coin's 30-day (180-bar) average 4h bar range -> replaced: the catalogue has only the 180-bar total high-low span (`RangeCompressionRatioComponent`) or close-to-close volatility (`VolatilityRatioToAverageComponent`), not the mean bar range.
- Outcome: the coin rises over the next three days (18 bars), more the narrower the stretch -> kept: an 18-bar long hold sized by the forecast.
- Verdict transfer: no: with the narrowness measured against a 30-day span or a return volatility, a reject would not say whether stretches narrow against the average 4h range lead to larger rises.
Reason: No catalogue component compares a stretch's range with the average 4h bar range (mean of high minus low over 180 bars). The forecast is a weighted mean, so it cannot make the breakout's size grow with narrowness; that would need a product inside one component.
