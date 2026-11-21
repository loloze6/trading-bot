---
idea: 016-05_up-even-volume-continuation.g1_evening-utc-hour-drift.d1_late-evening-rise-in-volatile-coins
brief: 016_grind-versus-jump-moves
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: untestable
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: the two hours after 21:00 UTC, scaled by realised hourly volatility over the past 7 days as its own level -> replaced: the hour window is kept as a regime (coming bars 21:00 and 22:00), but `standardise` turns the 168-bar volatility into a ratio to its own past values, which is the "against its recent past" reading the idea excludes.
- Comparison: the coin's rise in its other hours -> kept: the regime is long only in 21:00–23:00 and flat elsewhere, judged against holding the coin.
- Outcome: the coin rises over those two hours, more with higher volatility -> kept: 2 bars on 1h bars, long side.
- Verdict transfer: no: the size would follow volatility relative to its past, not its level, so neither result would settle the idea's volatility claim.
Reason: The idea sizes the evening long by the 7-day realised volatility taken as its own level, not against its recent past. The guide's hard rule makes `standardise` the first transform of every component, and it divides each value by the mean of the component's own past values. So no config can grade the position by the absolute volatility level, which is a limit of the config's logic, not a missing component.
