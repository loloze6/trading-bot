---
idea: 006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise.g2_volume-surge-widens-moves
brief: 006_range-compression-precedes-expansion
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: untestable
catalogue: 4e6cc97f57e5
---
Fidelity:
- Situation: the 5-day average volume is high against the 30-day average -> kept: VolumeRatioComponent with short_period 5 and period 30 measures it as stated.
- Comparison: the move after a higher volume ratio is compared with the move after a lower one -> kept: the graded size of the ratio carries this comparison.
- Outcome: a larger absolute price move over the next 3 days, in either direction -> replaced: a spot position can only gain from a signed move, not from the size of a move.
- Verdict transfer: no: a long or short position's gain measures direction, so it cannot confirm or reject a claim about move size regardless of direction.
Reason: The idea predicts how large the next 3-day move will be, not which way it goes, so the position it calls for is a bet on volatility, like a straddle. The config can only hold a long or short position in the coin, which gains only when the price moves its way. No forecast built from the catalogue can make the portfolio gain from a large move in either direction, so the idea's outcome cannot be expressed in this config.
