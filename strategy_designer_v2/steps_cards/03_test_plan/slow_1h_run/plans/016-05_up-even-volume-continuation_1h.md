---
idea: 016-05_up-even-volume-continuation
brief: 016_grind-versus-jump-moves
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: missing-components
catalogue: 4e6cc97f57e5
---
Fidelity:
- Situation: the coin has risen over the past 3 days, with its hourly volume spread more or less evenly across those hours -> adapted: a 72-bar rise becomes a regime, and the catalogue holds no graded measure that grows with volume evenness.
- Comparison: more even volume against less even volume, among rising coins -> kept: it is carried by the size of the position inside the up regime.
- Outcome: the coin keeps rising over the next 3 days, more so the more even the volume -> kept: the next 72 bars' return, long side.
- Verdict transfer: no: the test can only be faithful if a long position grows with evenness, and no component or allowed combination supplies that.
Reason: The rise maps to a regime rule (`PriceEvolutionComponent` at period 72, raw value at least 0). The forecast inside that regime then needs a positive, graded measure that grows with how evenly volume was spread over the 72 hours. The nearest component, `VolumeRatioComponent` (short_period 72, period 72, statistic "median", form "log"), gives ln(mean/median). That is a burstiness measure, almost always at or above 0. Negated, it is always short. Turning it into a long signal needs a constant offset, and a constant is not allowed inside a regime. So no catalogue component or combination gives a long position that grows with evenness.
