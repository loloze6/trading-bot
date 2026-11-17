---
idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.g1_next-day-rebound-after-sharp-falls.g1_rebound-grows-with-volatility
brief: 013_anchoring-to-recent-high
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
---
Fidelity:
- Situation: a one-day fall, measured against the coin's 20-day volatility of daily returns -> kept: `VolatilityScaledReturnComponent` (period 1, vol_period 20), negated so that falls are positive.
- Comparison: the rebound per unit of fall grows as 20-day volatility rises against its own past 120 days -> replaced: the config can only take weighted sums of components, so the fall can be added to a volatility rank but not multiplied by it.
- Outcome: the coin's return over the next 1 day is higher, upward (1 bar) -> kept: measured as the forward 1-bar return.
- Verdict transfer: no: without the product, the test checks only the plain rebound and not the volatility-dependent slope that is the idea's claim.
Reason: The idea needs the fall's size multiplied by the 20-day volatility's rank within its past 120 days. The forecast is a weighted sum of components, so it cannot form that product. The only multiplication the config has, `score_product`, sits in the regime detector and can only switch the position on or off. All the inputs are in the coin's own closes, and one component could compute the product directly.
