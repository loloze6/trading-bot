---
idea: 013-05_longer-stall-bigger-breakout
brief: 013_anchoring-to-recent-high
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
---
Fidelity:
- Situation: a close above the prior 52-week high -> adapted: "after the break" made "while the close is at its 365-bar high", as a regime rule on DistanceFromHighComponent(365) >= 0.
- Comparison: the number of days in the past 60 spent closing just under that high -> replaced: no catalogue component counts these days, and the depth or range position at one bar is a different quantity.
- Outcome: a larger return over the next 30 days, upward -> kept: the 30-bar forward return on 1d bars.
- Verdict transfer: no: the stall count that grades the idea cannot be built, so a test on a substitute would neither confirm nor reject it.
Reason: The idea's grading is a count, over the last 60 bars, of closes that sat just below the prior 52-week high. No component computes this count. The one history op that could accumulate it, `ema`, cannot sit alongside `standardise` in `transforms` (V15) and gives nothing useful in `history_transforms`. The breakout itself can be gated with DistanceFromHighComponent(365).
