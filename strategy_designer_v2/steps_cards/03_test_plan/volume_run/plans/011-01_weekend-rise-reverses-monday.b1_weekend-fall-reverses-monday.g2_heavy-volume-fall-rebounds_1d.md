---
idea: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.g2_heavy-volume-fall-rebounds
brief: 011_weekend-moves-reverse-weekday
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
---
Fidelity:
- Situation: a down day whose volume is high relative to its median daily volume over the past 20 days -> replaced: no component computes a median volume, and VolumeRatioComponent divides by the 20-bar mean, which includes the day itself.
- Comparison: that day's volume against the coin's 20-day median daily volume -> replaced: the median would become a mean, a different statistic for skewed crypto volume.
- Outcome: the coin rises over the next 1 day, more so the heavier the volume -> kept: a graded long position held while the situation lasts, judged on the 1-bar forward return.
- Verdict transfer: no: a test against mean volume, which spikes pull upward, would judge a different measure from the median-relative volume the idea names.
Reason: The down day (a regime rule on a 1-bar PriceEvolutionComponent) and the next-day long are expressible. However, no catalogue component measures volume against its rolling median, and VolumeRatioComponent's mean is a different quantity, not an allowed adaptation.
