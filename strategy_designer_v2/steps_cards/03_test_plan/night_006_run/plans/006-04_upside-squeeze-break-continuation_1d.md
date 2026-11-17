---
idea: 006-04_upside-squeeze-break-continuation
brief: 006_range-compression-precedes-expansion
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
---
Fidelity:
- Situation: the coin closes above the high of a tight 20-day band -> adapted: a graded reading of where the close sits in its 20-bar range, with the breakout end at the top of that range.
- Comparison: the narrower the 20-day band against the coin's 100-day range -> replaced: no catalogue component measures range width, so a volatility percentile would have to stand in for it.
- Outcome: price keeps rising beyond the band's top over the next 3 days -> kept: the long return over the next 3 bars, larger when the band was narrower.
- Verdict transfer: no: a test that sizes on standard-deviation volatility instead of the 20-to-100-day range ratio would not confirm or reject the idea as stated.
Reason: The idea sizes the bet by the width of the 20-day band divided by the width of the 100-day range, and that ratio comes from the coin's own high and low columns. No catalogue component outputs a range width, and the config's weighted sums and products cannot divide one range by another, so this needs a new graded component.
