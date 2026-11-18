---
brief: 005_rsi-divergence-predicts-reversal
source-idea: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g1_calm-regime-daily-move-continuation
line: 7.d not profitable
backtest: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g1_calm-regime-daily-move-continuation_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 20-day volatility is low relative to its last 100 days, a large one-day move continues in the same direction over the next 3 to 7 days, with the continuation building from the second day after the move onward. The larger the sum of the coin's last 5 daily moves, each relative to its 60-day mean absolute daily move and each weighted by how low the 20-day volatility rank was on its day, the larger the move over the next 5 days.
Consequence: A trader should keep following a calm-regime sharp move for several days after it, rather than for the single next day, which carries none of the continuation.
Why:
- F2: The position is held only on the day after the signal and never through the continuation. After a top-quintile |forecast| bar (n = 1170), 99.2% of positions are on the signal's side on day 1 (mean signed position 1.15). By day 2 that falls to 45% (mean signed position 0.012), and it stays near 0.01–0.06 through day 7.
- F3: The continuation the verdict confirmed is not on the day the book holds. After top-quintile bars, the signed excess return is 0.00033 on day 1 (t = 0.29, n = 1170). It is 0.0042 on day 2 (t = 3.81), 0.0021 on day 3 (t = 1.96) and 0.0028 on day 5 (t = 2.43). So the book trades the one day without the effect and is out for the days that carry it.
- F4: The forecast is a one-day spike: its correlation with the previous bar's forecast is 0.013 and its sign changes on 54% of bars. In the top quintile the position changes by 1.15 of the book per bar, for a fee of 0.00094 per bar.
- F1: The book earns almost nothing before fees and loses after them: its mean gain before costs is 0.000363 per bar against a mean fee of 0.000378, so its daily Sharpe is -0.016 against 0.64 for holding the coins.
