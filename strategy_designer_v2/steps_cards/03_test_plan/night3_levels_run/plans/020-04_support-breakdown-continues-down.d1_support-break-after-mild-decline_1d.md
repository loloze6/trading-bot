---
idea: 020-04_support-breakdown-continues-down.d1_support-break-after-mild-decline
brief: 020_support-and-resistance-at-past-turning-prices
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: e48527ec0eac
---
Fidelity:
- Situation: the close sits below a price where the coin turned up several times in the past 90 days -> adapted: "after the close breaks below" is measured as "while the close is below". `TouchWeightedSupportBreakDepthComponent` (period 90) gives the touch count times the depth below the level.
- Comparison: the more times the level held, the larger the fall, but the larger the past 10-day fall, the smaller the continuation -> replaced: the weighted mean can only add a 10-day fall term, which goes long with no break, and cannot multiply it into the break.
- Outcome: the price keeps falling over the next 5 days -> kept: a short held 5 bars on daily bars.
- Verdict transfer: no: a forecast that adds the prior 10-day fall instead of damping the break by it would go long on plain falls, so its result says nothing about the idea.
Reason: The idea needs the support-break reading shrunk by the size of the prior 10-day fall, so the position is zero when there is no break. The config's only combination is a weighted sum, with no product of components. Adding a 10-day fall component (`PriceEvolutionComponent` 10, negated and clipped) turns flat bars into longs. A regime veto on the fall would replace the graded damping with an on/off cut.
