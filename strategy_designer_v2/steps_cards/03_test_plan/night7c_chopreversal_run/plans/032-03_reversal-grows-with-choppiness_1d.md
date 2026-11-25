---
idea: 032-03_reversal-grows-with-choppiness
brief: 032_agitated-chop-weekly-reversal
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: 051b3422f169
---
Fidelity:
- Situation: a 7-day move scaled by the 30-day typical daily swing, in a 30-day window whose swings are large against its net move -> replaced: the config can only add the scaled move and the choppiness, not multiply them.
- Comparison: more agitated and trendless 30 days against less agitated or trending ones -> replaced: regime tiers would turn the graded growth into a few fixed bins.
- Outcome: the share of the 7-day move given back over the next 7 days grows with agitation -> kept: the 7-bar forward return against the sign of the scaled move.
- Verdict transfer: no: a weighted sum or tiered regimes cannot make the reversal grow with choppiness, so neither result would bear on the idea.
Reason: The idea is an interaction: the reversal bet must grow with both the scaled 7-day move and the 30-day choppiness. The config combines components only by a weighted mean, and score_product only gates regimes, so no catalogue component or combination computes that product. The nearest products in the catalogue (RangeShareHump, FlatnessWeightedRangePosition, MeanAbsScaledReturnTimesVolatility) weight a different move, or weight by a hump or by volatility rather than by trendlessness.
