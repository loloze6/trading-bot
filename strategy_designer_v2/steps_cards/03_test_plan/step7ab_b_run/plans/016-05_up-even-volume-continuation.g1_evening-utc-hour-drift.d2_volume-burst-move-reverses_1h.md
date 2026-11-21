---
idea: 016-05_up-even-volume-continuation.g1_evening-utc-hour-drift.d2_volume-burst-move-reverses
brief: 016_grind-versus-jump-moves
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: missing-components
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: a 3-day move with a large share of its 3-day volume in its single busiest hour -> adapted: the busiest-hour share (72 bars, top 1) graded, times the signed 72-bar move.
- Comparison: larger busiest-hour share against smaller, for the same 3-day move -> kept: the forecast's size grows with the share.
- Outcome: the coin gives back part of its 3-day move over the next 7 days -> kept: a position against the move, held 168 bars.
- Verdict transfer: no: the catalogue has no component that gives the forecast's direction (the move) scaled by the volume share, so no config can compute the idea's forecast.
Reason: The forecast needs the 72-bar move multiplied by the busiest-hour volume share. The engine only adds components by weight, and a score-product regime chooses a regime without scaling the forecast. Adding the direction-free share to the move does not give their product. A regime that switches on a high share would turn the idea's graded "the larger the share, the more" into a threshold, and that is not an allowed adaptation. `TopVolumesShareComponent` (period 72, top_k 1) and `PriceEvolutionComponent` (period 72) each exist, but no component and no composition combines them.
