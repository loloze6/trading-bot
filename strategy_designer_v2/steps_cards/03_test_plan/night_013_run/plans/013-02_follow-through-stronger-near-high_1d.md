---
idea: 013-02_follow-through-stronger-near-high
brief: 013_anchoring-to-recent-high
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
---
Fidelity:
- Situation: a coin's past 30-day return, while it closes some distance below its 52-week high -> kept: PriceEvolutionComponent(period 30) and DistanceFromHighComponent(period 365) on daily closes.
- Comparison: the return carries on more strongly the closer the close is to the high, and less the further below -> replaced: no component or combination scales the return by closeness, because the forecast can only add components.
- Outcome: the next 30 days continue the past 30-day return's direction -> kept: the 30-bar forward return, signed by the forecast.
- Verdict transfer: no: a sum of momentum and closeness is not the idea's interaction, so its result says nothing about the idea.
Reason: The idea needs the past 30-day return multiplied by closeness to the 365-day high. The config can only take a weighted sum of components, and `score_product` exists only in the regime detector. The sum (momentum plus distance) does not express the interaction, and nor does the Donchian position. Regime bands on distance would replace the graded closeness with thresholds and leave the position the same size in every band.
