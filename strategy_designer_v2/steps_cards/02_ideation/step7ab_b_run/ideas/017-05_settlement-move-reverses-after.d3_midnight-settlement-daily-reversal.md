---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after
line: 7.d not profitable
backtest: 017-05_settlement-move-reverses-after_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The 2-hour return into the 00 UTC funding settlement runs opposite to the return over the 24 hours after it, and the larger the pre-settlement move relative to the coin's usual 2-hour move, the larger the move back.
Consequence: If the settlement flow matters at all, it is at the daily 00 UTC settlement and over a day, not at every settlement over 2 hours.
Why:
- F2: The reversal after settlement is real but small. Signed by the 2-hour move into settlement, the next 2 hours return 3.5 bps on average (t 5.57 over about 52,000 settlement bars). Even the largest tenth of pre-settlement moves (354 bps on average) gives back only 10.0 bps over 2 hours and 22.7 bps over 8 hours, at most about one round trip.
- F4: Among settlement times, only the one at 00 UTC shows a lasting give-back. It returns 6.8 bps over 2 hours and 12.0 bps over 8 hours. The 08 UTC settlement returns 0.8 and −2.8 bps, and the 16 UTC one 3.6 and 7.3 bps.
- F5: The reversal reaches a size that pays only for the most extreme moves, and it keeps growing for a day. This was measured at all hours on a non-overlapping 8-hour grid:
