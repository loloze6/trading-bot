---
brief: 005_rsi-divergence-predicts-reversal
source-idea: 005-02_bullish-rsi-divergence-rebound
line: 7.d not profitable
backtest: 005-02_bullish-rsi-divergence-rebound_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's close makes a new 30-day low while its 14-day RSI is above its reading at the previous low in that window, the price rebounds over the next 20 days rather than on the next day. The further the RSI stays above its earlier trough, and the deeper the coin's 30-day decline into that low, the larger the rebound.
Consequence: The divergence low is a reason to stay long through the following weeks of a deep fall, not for one day, and to refuse it when the preceding fall was shallow.
Why:
- F1: The book was almost never in the market, so it could not earn the effect it bets on. It held a position on only 1.4% of its 5794 coin-days, with a mean position of 0.25 when held. After a divergence signal the position lasted a mean of 0.91 bars (median 1, max 8), because the forecast is non-zero only on the new-low bar itself. The mean daily return was -0.0000034 and the Sharpe was -0.04.
- F2: The book only captured the next day, and that day loses. After the 44 independent divergence new lows, the next 1-day return averaged -0.49% (t -0.82). The 10-day return averaged +1.22% (t 0.56), against -2.66% for the 43 new lows without divergence. The 20-day return averaged +5.60% (t 1.37, n=38), against -3.00% without divergence.
- F3: Inside the divergence cases, the depth of the prior 30-day fall grades the rebound. The deepest tercile of 30-day return (mean -34%) gained +4.56% over 10 days, +3.28% above the coin's mean (t 0.82, n=15). The shallowest tercile (mean -9.9%) lost -2.24%, -3.49% below the coin's mean (t -1.37, n=15). The Spearman correlation of the 14-day return with the 10-day return was -0.31.
- F4: The forecast's own size barely grades the outcome. Its Spearman correlation with the 10-day excess return over the 44 divergence cases is only 0.16 (Pearson 0.08).
