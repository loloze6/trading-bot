---
idea: 022-03_combined-extremes-larger-moves.b1_past-weighted-reversal-20-days.d1_weighted-reversal-with-trend-agreement
brief: 022_weak-effects-combined-by-what-worked-before
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: 7b01a83193f3
---
Fidelity:
- Situation: the 1-day return term (365-day z-score times its 365-day correlation with the next 5 days' return) far from its usual value -> adapted: graded by the "single"/"reversal" term of `PastPredictivePowerWeightedCompositeComponent` (365, 365, 5), with the far-out tail stressed by `signed_power` instead of a "far from usual" threshold.
- Comparison: the move is larger the more the coin's own 60-day return points in the term's direction -> replaced: no component multiplies the term by its agreement with the 60-day return, and a weighted sum would bet on the 60-day trend alone when the term is zero.
- Outcome: the coin moves in the term's direction over the next 20 days, more the further out the term -> kept: a 20-bar horizon on daily bars, with gains growing with the size of the position.
- Verdict transfer: no: without the interaction, a test of the term alone, or of the term plus the trend, would not test the claim that trend agreement enlarges the term's move.
Reason: The 60-day agreement works as a multiplier on the term's predicted move, and the config's logic is a weighted mean, so it can only add the term and the 60-day return. The only product modes sit in the regime detector, which classifies a bar and cannot set the size of a position. Everything needed is in each coin's own daily closes, so one component that computes the product would make the idea testable.
