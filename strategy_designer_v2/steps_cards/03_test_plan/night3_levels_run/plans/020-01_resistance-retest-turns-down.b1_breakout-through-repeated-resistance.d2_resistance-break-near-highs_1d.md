---
idea: 020-01_resistance-retest-turns-down.b1_breakout-through-repeated-resistance.d2_resistance-break-near-highs
brief: 020_support-and-resistance-at-past-turning-prices
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: e48527ec0eac
---
Fidelity:
- Situation: a close above a price where the coin turned down several times in 90 days, after closing below it the day before -> adapted: graded by the level's touch count times the close's margin above it (`ResistanceBreakTouchCountComponent`, period 90, cross_period 1).
- Comparison: the rise is larger the nearer that close is to the 60-day highest close -> replaced: the config cannot multiply this nearness into the break; it can only add it or gate on it by a threshold.
- Outcome: the coin rises over the next 10 days -> kept: a long held for 10 bars.
- Verdict transfer: no: without the nearness weighting the break, the test cannot check the idea's claim that breaks far below the 60-day high fail.
Reason: The idea's forecast is the product of the break's touch-weighted strength and the close's nearness to its 60-day high close. A strategy only takes weighted sums of components. A sum would hold positions on days with no break. A threshold gate on the nearness would drop the graded "the more so". No single component computes the product.
