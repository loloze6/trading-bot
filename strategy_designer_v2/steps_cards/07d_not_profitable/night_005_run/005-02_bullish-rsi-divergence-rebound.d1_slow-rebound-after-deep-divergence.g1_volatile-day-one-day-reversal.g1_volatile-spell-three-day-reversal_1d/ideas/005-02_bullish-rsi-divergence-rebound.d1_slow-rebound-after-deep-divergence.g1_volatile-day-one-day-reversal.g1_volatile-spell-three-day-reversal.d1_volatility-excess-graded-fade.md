---
brief: 005_rsi-divergence-predicts-reversal
source-idea: 005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence.g1_volatile-day-one-day-reversal.g1_volatile-spell-three-day-reversal
line: 7.d not profitable
backtest: 005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence.g1_volatile-day-one-day-reversal.g1_volatile-spell-three-day-reversal_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's 20-day volatility is high relative to its 60-day average, its return over the next 3 days runs against the day just closed. The larger that day's return relative to its 20-day volatility, the larger the move back. The move back grows with how far the 20-day volatility stands above its 60-day average: it is small when the two are close and largest when the 20-day volatility is far above it.
Consequence: A trader leans against a large daily move only lightly when volatility has just crept above its average, and hard when it stands far above. This avoids paying fees in mildly volatile spells.
Why:
- F2: The gain sits only where volatility is well above its average. Active bars were split into quarters by volatility ratio, with these mean ratios and daily results:
- F3: The positions were rescaled on the same daily returns and the same fee rate (0.082% per unit of turnover):
- F1: The book did not fail on its forecast but on how far it falls. Its deepest fall was -34.0% over 277 days across w10–w13. Over that same stretch the coins themselves rose 0.39% a day. Of the fall's net loss, -0.304 came from shorts taken while the coin's 20-day return was negative, over 50 days with a volatility ratio near 1.14. All the other position types made money in that stretch (longs +0.058 and +0.263, shorts in rising 20-day trends +0.046).
