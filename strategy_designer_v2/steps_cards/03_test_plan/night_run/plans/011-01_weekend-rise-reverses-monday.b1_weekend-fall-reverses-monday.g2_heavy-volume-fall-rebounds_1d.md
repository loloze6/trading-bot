---
idea: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.g2_heavy-volume-fall-rebounds
brief: 011_weekend-moves-reverse-weekday
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
---
Fidelity:
- Situation: a down day, graded by its volume relative to the 20-day median daily volume -> replaced: no catalogue component measures volume against its median. The down day alone could be a regime rule.
- Comparison: higher relative volume against lower relative volume on down days -> replaced: it needs the same missing relative-volume measure.
- Outcome: the coin rises over the next 1 day, more so with heavier volume -> kept: 1 bar on daily bars.
- Verdict transfer: no: without a relative-volume measure, the test cannot grade the position by the idea's volume condition.
Reason: The idea's situation is graded by the day's volume divided by its 20-day median volume. The only volume-reading parts are the VolumeExpansionHedgeComponent, which is on/off, fires on up bars and uses the mean, and the volume_filter op, which is on/off, uses the mean and is a dead zone. Neither can be combined into a graded volume/median ratio. The down day itself can be expressed as a regime rule on PriceEvolutionComponent with period 1.
