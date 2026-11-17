---
idea: 006-01_compression-precedes-larger-move
brief: 006_range-compression-precedes-expansion
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: untestable
---
Fidelity:
- Situation: 20-day average high-low range narrow against its 100-day range, and 20-day volume fallen against 100-day volume -> replaced: no catalogue component computes a high-low range ratio or a volume ratio; the nearest are close-based volatility and on/off volume.
- Comparison: the move after compression against the move after normal activity -> kept: the forecast's size would grade the compression against each coin's own past.
- Outcome: a larger absolute price change over the next 5 days, in either direction -> replaced: a position earns only on direction, so it cannot bet on the size of a move.
- Verdict transfer: no: the config's gains depend on getting the direction right, and the idea says the direction is unknown.
Reason: The idea predicts the size of the next 5-day move, not its direction, but the config can only hold a long or short position, which gains only when its side matches the price's direction; a bet on size alone, such as a straddle, cannot be expressed. The situation's high-low range ratio and volume ratio are also not computed by any catalogue component, but the directionless outcome alone makes the idea untestable here.
