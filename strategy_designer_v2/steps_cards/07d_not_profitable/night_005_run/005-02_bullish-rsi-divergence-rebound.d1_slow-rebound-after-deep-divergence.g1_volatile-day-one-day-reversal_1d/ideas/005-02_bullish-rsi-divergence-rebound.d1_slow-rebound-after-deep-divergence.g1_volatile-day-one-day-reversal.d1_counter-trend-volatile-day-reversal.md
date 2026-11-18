---
brief: 005_rsi-divergence-predicts-reversal
source-idea: 005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence.g1_volatile-day-one-day-reversal
line: 7.d not profitable
backtest: 005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence.g1_volatile-day-one-day-reversal_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: On a coin's high-volatility days, measured by its 20-day volatility, the next day's return runs against the day just closed, only while that day's move runs against the coin's 20-day return. The larger that day's return relative to its 20-day volatility, the larger the move back over the next 1 day.
Consequence: A trader leans for one day against a large counter-trend day in a volatile spell, such as a sharp drop inside a 20-day rise, and refuses to fade a large day that goes with the 20-day trend.
Why:
- F3: Among high-volatility bars in the top two |z| quintiles, the move back holds only when the day ran against the coin's 20-day return.
- F1: The gain sits only in the largest scaled moves: among active bars, the top quintile of |day's return / 20-day volatility| (mean |z| 1.87) earns 0.00477 a bar before fees (t 2.77, n 574) and 0.00406 after fees. The four lower quintiles earn 0.00009 to 0.00103 before fees against fees of 0.00031 to 0.00053, so three of the four lose net (-0.00022, -0.00010, -0.00040).
- F5: The deepest falls are long and slow rather than single shocks.
