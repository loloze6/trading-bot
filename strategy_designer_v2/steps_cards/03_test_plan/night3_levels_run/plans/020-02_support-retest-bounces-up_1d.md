---
idea: 020-02_support-retest-bounces-up
brief: 020_support-and-resistance-at-past-turning-prices
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: price falls back to a price where it turned up several times in the past 90 days -> replaced: no catalogue component finds past turning points or counts them near the current price.
- Comparison: the more times it turned up there before, the larger the rise -> replaced: no component grades by the number of past turns at a level.
- Outcome: it rises over the next 5 days -> kept: a 5-bar forward rise on daily bars.
- Verdict transfer: no: a test that only used the distance from the 90-day low would measure one extreme, not a level that held several times, so its verdict would not carry over to the idea.
Reason: The idea needs, for one coin, the number of past 90-day turning-up points (swing lows) near the current close, reached from above. That comes from the coin's own bars and could be a graded component, but no catalogue component computes it. The closest fits measure other things: `DistanceFromHighComponent` (extreme "low") measures the distance to the single lowest low, and `StallUnderHighCountComponent` counts bars stalled under a high, not turns. No combination of them counts reversals at a price.
