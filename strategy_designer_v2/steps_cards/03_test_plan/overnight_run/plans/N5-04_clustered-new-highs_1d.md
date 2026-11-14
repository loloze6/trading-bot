---
idea: N5-04_clustered-new-highs
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
---
Fidelity:
- Situation: a coin keeps printing new 20-day closing highs, each within ten days of earlier ones -> replaced: `BarsSinceHighComponent` sees only the latest high, so it cannot tell a run of highs from a first break.
- Comparison: the coin's average 10-day rise -> kept: holding the coin is the baseline in the criterion.
- Outcome: the 10-day forward rise is larger, upward -> kept: the forward 10-bar return after the situation.
- Verdict transfer: no: a forecast built on the latest high's recency also includes first breaks, which the idea explicitly sets apart.
Reason: The idea needs to know whether the latest new 20-day closing high came within ten bars of earlier ones, which is a count or spacing of several highs. No catalogue component, alone or combined, measures more than the most recent high (`BarsSinceHighComponent`) or the close's place in its range (`DonchianBreakoutComponent`). All of it can be computed from the coin's own closes, and the config's logic could hold it as a graded value.
