---
idea: 020-03_resistance-breakout-continues-up
brief: 020_support-and-resistance-at-past-turning-prices
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: a close above a price where the coin turned down several times in the past 90 days -> replaced: no component finds past turn-down prices or a close crossing them; only the 90-day high or near-high bar counts exist.
- Comparison: the more times the level held before, the larger the rise -> replaced: no component counts how often price turned down at one level.
- Outcome: keeps rising over the next 5 days -> kept: a 5-bar forward return, long side.
- Verdict transfer: no: a 90-day-high breakout or near-high stall count is a different situation, so its result would not settle the idea.
Reason: The situation and its grading need the past swing highs (bars where the close turned down) grouped by price level over the last 90 bars, and a check that the current close has crossed above such a level. All of this is in one coin's own bars and a component could output it. No catalogue component or combination finds turning points or counts touches at a level: `DistanceFromHighComponent` and `StallUnderHighCountComponent` only read the single highest close, not repeated reversal prices.
