---
brief: 005_rsi-divergence-predicts-reversal
source-idea: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal
line: 7.d not profitable
backtest: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's 1-day fall relative to its own 20-day daily volatility, and the nearer its close to the day's low, the more it rises over the next 1 day; the larger its vol-scaled 1-day rise, the more it gives back over the next 1 day, only while its 20-day return is negative, and the more so the deeper that 20-day fall.
Consequence: A trader should keep buying outsized down days but fade outsized up days only inside a 20-day decline. This drops the short trades that lose to the market's rise and much of the daily turnover that the fees eat.
Why:
- F1: Before fees the book earns too little to pay its trading: it gains 0.000231 a bar (t 1.19, n 5794) but pays 0.00036 a bar in fees, so it loses 0.000129 a bar. Its daily book returns average -0.000324 on BTC and 0.000057 on ETH, while holding the coins earns 0.00118 and 0.00137.
- F2: The fees are high because the book turns over almost its whole position every day. The mean trade is 0.44 of the book against a mean held position of 0.32, and 52% of bars flip the position's side.
- F3: The short side, the give-back after up days, carries the loss. Short bars lose 0.000281 a bar before fees (t -1.20, n 2958) and 0.000636 after. Long bars gain 0.000769 before fees (t 2.44, n 2823) and 0.000403 after.
- F4: The short side's loss is mostly the market's own rise, not bad timing. The market-rise part of short bars is -0.000368 a bar, larger than their whole gross loss of -0.000281.
- F5: The short side loses most when the coin's 20-day return is positive: -0.000585 a bar before fees and -0.000941 after (n 1419). When the 20-day return is negative it is flat, at -0.00000001 before fees (n 1539).
- F6: The give-back after up days appears only when the coin has been falling over 20 days. In the weakest quarter of 20-day vol-scaled return, up days are followed by a next-day excess return of -0.00546 (t -2.57, n 491). In the strongest quarter they are followed by +0.000226 (t 0.17, n 729).
- F7: In a falling 20-day trend, up days of 0 to 1 usual moves are followed by -0.00389 (t -2.62, n 804). In a rising trend the same days are followed by +0.000988 (t 0.92, n 955).
- F8: The rebound after down days holds across trends and is graded by the size of the fall. The product of minus the vol-scaled move and the next-day excess return has t 2.22 (n 2340) in falling 20-day trends. Down days are followed by +0.00353 (t 2.11, n 480) in the strongest uptrend quarter and by +0.00273 (t 1.51, n 718) in the weakest.
