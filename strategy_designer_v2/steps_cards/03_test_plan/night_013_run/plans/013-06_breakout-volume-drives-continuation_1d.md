---
idea: 013-06_breakout-volume-drives-continuation
brief: 013_anchoring-to-recent-high
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
---
Fidelity:
- Situation: a close above the prior 52-week high -> adapted: "after X" becomes "while X", using a regime on `BarsSinceHighComponent` (lookback 365 bars) that is active on the breakout bar.
- Comparison: breakout-day volume against its own 90-day average, graded -> replaced: no catalogue component measures volume relative to its average.
- Outcome: a larger return over the next 30 days the higher that volume ratio -> adapted: the 30-bar holding period is dropped and measured as a 30-bar forward return.
- Verdict transfer: no: without the volume ratio, the config can only test breakouts in general, not whether heavier breakout volume brings larger follow-through.
Reason: The idea's graded strength is the breakout bar's volume divided by its 90-day average volume. No catalogue component outputs a graded volume ratio: `VolumeExpansionHedgeComponent` is on/off and only fires on low-volume up bars, and `volume_filter` is a dead zone that cannot be used in `strategies`. No combination of price-based components can produce it, even though the volume column is in every coin's own bars.
