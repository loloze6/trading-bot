---
idea: 006-02_longer-squeeze-bigger-move
brief: 006_range-compression-precedes-expansion
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: untestable
---
Fidelity:
- Situation: the number of the past 60 days whose closes stayed inside a band that is narrow against the 100-day range -> replaced: no catalogue component counts days inside a band, so a volatility rank would stand in for it.
- Comparison: the band's width against the coin's own 100-day range -> replaced: by a volatility percentile, not a range-width ratio.
- Outcome: a larger absolute price change over the next 5 days, in either direction -> replaced: a position earns only from direction, so it cannot capture an absolute move.
- Verdict transfer: no: a long or short book cannot confirm or reject a prediction about the size of a move whose direction the idea says is unknown.
Reason: The idea predicts how large the next 5-day move is, not which way it goes. The config only sets a long or short position, which gains only when its side matches the price's direction, so it cannot bet on the size of a move regardless of direction (a straddle-like volatility payoff). The compression count would also need a component the catalogue lacks, but the direction-free outcome is the deciding limit.
