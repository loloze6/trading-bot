---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d2_reversal-shorts-in-downtrends.b1_nearness-reversal-more-coins
line: 7.g patterns
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d2_reversal-shorts-in-downtrends.b1_nearness-reversal-more-coins_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 20-day return is negative, the larger its 5-day return relative to its 20-day volatility, the larger its fall over the next 5 days.
Consequence: A trader would short sharp bounces inside a coin's downtrend, sized by the bounce's strength, and would not chase them long.
Why:
- F4: In coins whose 20-day return is negative, the larger the 5-day return scaled by 20-day volatility, the larger the drift-removed fall over the next 5 days: rho -0.074 (t -3.28, 1974 cases). The top quintile, the sharpest bounces, falls -1.82 % beyond drift (t -3.40). Rho is negative in 14 of 15 coins. In coins whose 20-day return is not negative the relation is absent (rho +0.006, t 0.28).
- F7: The book lost money in short holds and made it in long holds. Shorts closed within about 5 days lost -3.36 % net on average (705 trades). Shorts held over 20 days gained +6.19 % (259 trades, median +9.50 %). The book's mean daily return was -0.002 %, and its best 2 % of days came when the coins fell -8.3 % on average.
