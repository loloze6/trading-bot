---
brief: 005_rsi-divergence-predicts-reversal
source-idea: 005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence.g1_volatile-day-one-day-reversal
line: 7.d not profitable
backtest: 005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence.g1_volatile-day-one-day-reversal_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: On a coin's high-volatility days, measured by its 20-day volatility, the next day's return runs against the day just closed. The larger that day's return relative to its 20-day volatility, and the higher the 20-day volatility stands above its 60-day average, the larger the move back over the next 1 day.
Consequence: A trader leans hardest against large daily moves when volatility has just expanded well above its usual level, and lets the lean shrink toward nothing as volatility returns to normal, which saves fees on bets too small to pay.
Why:
- F6: The gain rises with the volatility ratio: in the top quartile of 20-day volatility over its 60-day mean, active bars earn 0.0060 long and 0.0024 short. The lower quartiles earn between -0.0012 and +0.0017.
- F1: The gain sits only in the largest scaled moves: among active bars, the top quintile of |day's return / 20-day volatility| (mean |z| 1.87) earns 0.00477 a bar before fees (t 2.77, n 574) and 0.00406 after fees. The four lower quintiles earn 0.00009 to 0.00103 before fees against fees of 0.00031 to 0.00053, so three of the four lose net (-0.00022, -0.00010, -0.00040).
- F2: Fees eat 42% of the gain: across all bars they cost 0.000279 a bar against a gross gain of 0.000669. Trades come at 0.40 per bar, and in ETH's deepest fall the fees summed to 0.23 against a gain sum of -0.12.
