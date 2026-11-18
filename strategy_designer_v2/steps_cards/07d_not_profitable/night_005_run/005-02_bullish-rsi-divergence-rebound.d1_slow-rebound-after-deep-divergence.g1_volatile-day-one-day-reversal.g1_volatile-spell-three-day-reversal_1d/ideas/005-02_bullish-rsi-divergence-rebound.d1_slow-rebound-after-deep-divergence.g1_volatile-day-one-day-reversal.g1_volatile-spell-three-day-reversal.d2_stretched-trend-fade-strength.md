---
brief: 005_rsi-divergence-predicts-reversal
source-idea: 005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence.g1_volatile-day-one-day-reversal.g1_volatile-spell-three-day-reversal
line: 7.d not profitable
backtest: 005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence.g1_volatile-day-one-day-reversal.g1_volatile-spell-three-day-reversal_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's 20-day volatility is high relative to its 60-day average, its return over the next 3 days runs against the day just closed. The larger that day's return relative to its 20-day volatility, and the further the coin's 20-day return stands from zero in units of its 20-day volatility, the larger the move back.
Consequence: A trader fades large daily moves hardest when the coin is already stretched over the past 20 days, and lightly when its 20-day path is flat.
Why:
- F4: The fade pays most at the ends of the 20-day trend and loses in its middle. Active bars were split into fifths by 20-day return:
- F1: The book did not fail on its forecast but on how far it falls. Its deepest fall was -34.0% over 277 days across w10–w13. Over that same stretch the coins themselves rose 0.39% a day. Of the fall's net loss, -0.304 came from shorts taken while the coin's 20-day return was negative, over 50 days with a volatility ratio near 1.14. All the other position types made money in that stretch (longs +0.058 and +0.263, shorts in rising 20-day trends +0.046).
