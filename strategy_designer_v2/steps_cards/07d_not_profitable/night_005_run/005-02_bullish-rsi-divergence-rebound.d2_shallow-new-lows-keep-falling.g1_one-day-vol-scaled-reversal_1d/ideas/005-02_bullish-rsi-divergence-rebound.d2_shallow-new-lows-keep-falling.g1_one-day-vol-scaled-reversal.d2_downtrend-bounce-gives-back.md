---
brief: 005_rsi-divergence-predicts-reversal
source-idea: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal
line: 7.d not profitable
backtest: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's 1-day rise relative to its own 20-day daily volatility while its 20-day return is negative, and the deeper that 20-day fall, the more it falls over the next 1 day.
Consequence: A trader should treat a sharp one-day bounce inside a 20-day decline as a one-day selling opportunity, and refuse to buy it.
Why:
- F6: The give-back after up days appears only when the coin has been falling over 20 days. In the weakest quarter of 20-day vol-scaled return, up days are followed by a next-day excess return of -0.00546 (t -2.57, n 491). In the strongest quarter they are followed by +0.000226 (t 0.17, n 729).
- F7: In a falling 20-day trend, up days of 0 to 1 usual moves are followed by -0.00389 (t -2.62, n 804). In a rising trend the same days are followed by +0.000988 (t 0.92, n 955).
- F9: Over 3 days there is no reversal. Non-overlapping 3-day moves are followed by 3-day excess returns with |t| below 1 in every trend and move-size group, so the effect lasts only one day and cannot be traded more slowly to save fees.
