---
idea: 020-01_resistance-retest-turns-down.d1_breakout-beyond-90-day-high.d2_fresh-breakout-carries-further
brief: 020_support-and-resistance-at-past-turning-prices
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: e48527ec0eac
---
Fidelity:
- Situation: the daily close stands above its highest close of the previous 90 days, graded by how far -> adapted: graded distance; the level must be the 90-day high fixed on the day of the break, and no component holds it.
- Comparison: fewer days since the close first broke the 90-day high gives a stronger rise -> replaced: no catalogue component gives the age of the break, and the config cannot multiply distance by age.
- Outcome: the coin rises more over the next 20 days -> kept: horizon of 20 bars on 1d bars.
- Verdict transfer: no: the age and its interaction with the distance would have to be replaced by another quantity, so neither result would bear on the idea.
Reason: The idea is a function of one coin's closes. A single stateless component could compute it from the bar window. But no catalogue component measures the close's distance above the 90-day high fixed at the breakout, weighted by how few days have passed since that breakout. The config's weighted mean cannot form the product of two components. DistanceFromHighComponent (exclude_current 1) compares to a rolling high that later closes keep raising, so it is positive only on new-high bars. BarsSinceHighComponent counts bars since the last new high, not since the first break, and it is on/off as a forecast source.
