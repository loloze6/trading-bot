---
brief: 005_rsi-divergence-predicts-reversal
source-idea: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling
line: 7.d not profitable
backtest: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: The closer a coin's close is to its 30-day high close, the more it rises over the next 10 days.
Consequence: A coin trading near its 30-day high is a reason to hold it long, and one far below that high is a reason to hold less.
Why:
- F8: Across all bars on the non-overlapping 10-bar grid, the 10-bar return rises with closeness to the 30-day high close: 0.005 in the deepest quintile, 0.013 in the middle quintile and 0.023 at the high, with 103 cases each. Strength continues; weakness does not.
- F1: The book is in a position on only 5.1% of bars, at a mean absolute size of 0.26 of the book, so its mean daily return is 1.2e-5 against the coin's 0.00128, with a daily standard deviation of 0.0036 against 0.040; the failed mean-return and Sharpe-versus-holding measures come mainly from this near-permanent flatness.
- F2: The 299 active short bars sit against the coins' rise: the next-bar coin return on them averages +0.0008 (against +0.00128 on all bars). Gain per active bar is only 0.00048, and 181 trades of 1.74 days win 33% of the time.
- F7: The result rests on a few falling windows. w1 (+0.154) and w2 (+0.215) carry the summed book return, while w9 (-0.191) and w22 (-0.090) lose. Eight windows have 0 to 3 active bars, and the lowest Sharpe with one window left out is -0.18.
