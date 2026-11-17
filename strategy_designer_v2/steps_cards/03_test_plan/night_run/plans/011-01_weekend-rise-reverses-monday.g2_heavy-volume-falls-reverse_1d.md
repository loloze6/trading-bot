---
idea: 011-01_weekend-rise-reverses-monday.g2_heavy-volume-falls-reverse
brief: 011_weekend-moves-reverse-weekday
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
---
Fidelity:
- Situation: a coin's large one-day fall made on heavy volume -> adapted: the fall is graded as the one-bar return in usual moves, negated, but its volume weighting has no component.
- Comparison: that day's volume against its 60-day average volume -> replaced: no catalogue component measures volume against its own average, so nothing could stand in for it.
- Outcome: the fall is partly undone over the next 1 day (1 bar), more so the heavier the volume -> kept: a long position sized by the situation, judged on the next bar's return.
- Verdict transfer: no: without the volume comparison, a test would only measure one-day reversal of any fall, which neither confirms nor rejects the heavy-volume claim.
Reason: The idea's core is volume relative to its 60-bar average, which sits in the coin's own bars, but no catalogue component computes it. The only volume reader, VolumeExpansionHedgeComponent, is on/off and fires only on low-volume up bars, so neither a detector rule nor a strategy composition can grade a fall by heavy volume.
