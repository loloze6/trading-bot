---
idea: 022-03_combined-extremes-larger-moves.b1_past-weighted-reversal-20-days.d3_persistent-weighted-reversal-extremes
brief: 022_weak-effects-combined-by-what-worked-before
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: 7b01a83193f3
---
Fidelity:
- Situation: the 1-day-reversal term (365-day z-score times its 365-day correlation with the next 5 days' return) is far from its usual value -> adapted: the "single"/"reversal" term is graded with the strongest signed_power dead zone instead of a "far out" threshold.
- Comparison: the more of the past 20 days the term has stayed far out on the same side, the larger the move -> replaced: no catalogue component, alone or combined, counts the term's past days far out, so only today's term could stand in for it.
- Outcome: the coin moves in the term's direction over the next 20 days, more the further out the term -> kept: a 20-bar hold on daily bars, signed by the term.
- Verdict transfer: no: without the persistence count, the test would judge fresh extremes and lasting ones alike, which is the very distinction the idea makes.
Reason: The term is computed by `PastPredictivePowerWeightedCompositeComponent` (weighting "single", signal "reversal"), but nothing in the catalogue counts how many of the past 20 days it stayed far out on today's side. `standardise` must be the only history op in `transforms`, and history ops in `history_transforms` see one value, so no composition can count or smooth the term's own past values.
