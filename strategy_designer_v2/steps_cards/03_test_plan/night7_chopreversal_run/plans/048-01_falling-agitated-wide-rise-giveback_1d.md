---
idea: 048-01_falling-agitated-wide-rise-giveback
brief: 048_falling-agitated-wide-rise-giveback
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: e8f4c1171351
---
Fidelity:
- Situation: a day's rise against the 30-day daily swing, times its range against the 30-day usual range, in a falling agitated market -> replaced: no component computes this product; the nearest, `RiseTimesRangeMultipleComponent`, measures the rise in percent, not in 30-day swings.
- Comparison: the larger that product, the larger the fall -> adapted: graded, the short position grows with the product.
- Outcome: the coin falls over the next day -> kept: a short held 1 bar on daily bars.
- Verdict transfer: no: a rise in raw percent is a different measure from a rise in usual daily moves, so the test would not judge the idea as stated.
Reason: The idea's signal is the day's rise in 30-day standard deviations times the day's range in 30-day mean ranges. All of it comes from the coin's own daily bars. The forecast cannot multiply two components, so the product has to come from one component, and none gives it. `ScaledFallRangeMultipleComponent` gives exactly this product for falls only, and `RiseTimesRangeMultipleComponent` scales the rise by percent, not by the swing.
