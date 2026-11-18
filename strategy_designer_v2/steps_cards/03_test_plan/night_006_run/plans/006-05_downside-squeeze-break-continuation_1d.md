---
idea: 006-05_downside-squeeze-break-continuation
brief: 006_range-compression-precedes-expansion
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: 70a362722b07
---
Fidelity:
- Situation: a close below the low of the prior 20-day band -> replaced: no component compares the close with the prior 20-bar low; Donchian uses closes, not lows.
- Comparison: how narrow that 20-day band was against the 100-day range -> replaced: RangeCompressionRatio counts the breaking bar in its 20-bar band, not the band before the break.
- Outcome: price keeps falling beyond the band's bottom over the next 3 days -> kept: a short forecast held while the break lasts, judged over 3 bars.
- Verdict transfer: no: built from closes and a band that includes the break bar, the test would measure a different event, so neither result would settle the idea.
Reason: The break below the band's low and the band's narrowness before the break both come from the coin's own high, low and close. A regime rule plus a graded short component could hold them. But no catalogue component computes the close against the prior 20-bar low, and none measures compression with the current bar left out. Donchian (closes only) and DistanceFromHigh (highs only) do not combine into either one.
