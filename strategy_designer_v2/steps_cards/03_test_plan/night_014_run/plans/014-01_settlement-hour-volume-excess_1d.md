---
idea: 014-01_settlement-hour-volume-excess
brief: 014_funding-settlement-hour-pressure
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: untestable
catalogue: 791f9c660ae8
---
Fidelity:
- Situation: the two hours either side of each funding settlement (00:00, 08:00, 16:00 UTC), with a large absolute 3-day return going in -> replaced: daily bars hold no hourly volume, so the settlement hours cannot be separated.
- Comparison: volume in the settlement hours against the other hours of the same day -> replaced: one daily volume figure cannot be split between hours of the day.
- Outcome: excess volume around settlement, larger after a bigger absolute 3-day move, with no price direction -> replaced: the backtest only scores price direction, and a two-hour horizon is shorter than one 1d bar.
- Verdict transfer: no: a daily price-direction test can neither confirm nor reject a claim about intraday volume clustering.
Reason: The idea compares volume across hours of the same day, and its horizon is about two hours. Both are shorter than the 1d bar, so the coin's own bars cannot hold them. The idea also predicts volume, not a price direction, which is something the config cannot turn into a position that gains or loses.
