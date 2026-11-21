---
idea: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d2_extended-fall-daily-rebound
brief: 016_grind-versus-jump-moves
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: missing-components
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: the more the coin fell over the last 24 hours, at any hour -> kept: the 24-bar return (`PriceEvolutionComponent` period 24), negated and clipped at 0.
- Comparison: the rise is larger the more it also fell over the 48 hours before those 24 -> replaced: the catalogue only adds standardised components, so the prior 48-bar fall would add to the forecast instead of amplifying the 24-bar fall.
- Outcome: the coin rises over the next 1 to 2 days -> kept: a long held 48 bars.
- Verdict transfer: no: a sum of the two falls also goes long on a prior fall with no fresh 24-hour fall, so it would not test the claimed amplification.
Reason: The idea's comparison is an interaction: the 24-bar fall's effect grows with the fall over bars t-72 to t-24. A weighted mean, `signed_power` and `MomentumDivergenceComponent` (r24 x r72, which has no direction and is positive on joint rises) cannot form a directional product of the two falls. Both falls are in the coin's own closes, and the forecast could hold such a product as one graded component.
