---
idea: 016-08_down-volume-burst-reversal
brief: 016_grind-versus-jump-moves
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: missing-components
catalogue: 4e6cc97f57e5
---
Fidelity:
- Situation: the coin has fallen over the past 3 days (72 bars) -> kept: PriceEvolutionComponent with period 72, negative, in a regime rule.
- Comparison: a larger share of the period's volume traded in its few busiest hours -> replaced: no catalogue component, alone or combined, computes this share.
- Outcome: the coin wins back more of the fall over the next 3 days (72 bars), up -> kept: a long position judged on the 72-bar forward return.
- Verdict transfer: no: the graded quantity the idea turns on cannot be built, and any stand-in (such as the current bar's volume ratio) would test a different idea.
Reason: The idea needs the share of the last 72 hours' volume that sits in its few busiest hours, a top-k concentration of hourly volume within the window. No component ranks or sums the largest volumes within a window, and weighted means of the volume-ratio components cannot express a top-k share. The data needed (hourly volume) is in each coin's own bars, and a graded component in a regime gated on a 72-bar fall could hold it.
