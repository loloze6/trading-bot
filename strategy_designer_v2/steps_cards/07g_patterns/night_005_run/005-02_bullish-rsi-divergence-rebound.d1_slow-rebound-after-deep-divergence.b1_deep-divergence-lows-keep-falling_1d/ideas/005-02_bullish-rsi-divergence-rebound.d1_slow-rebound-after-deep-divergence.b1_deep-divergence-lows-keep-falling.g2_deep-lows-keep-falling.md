---
brief: 005_rsi-divergence-predicts-reversal
source-idea: 005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence.b1_deep-divergence-lows-keep-falling
line: 7.g patterns
backtest: 005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence.b1_deep-divergence-lows-keep-falling_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin closes at a new 30-day low, it falls further than its usual drift over the next 20 days, and the deeper its 30-day decline into that low, the larger the further fall, whatever its RSI shows.
Consequence: A deep new low is a reason to refuse to buy the turn, and the RSI divergence filter can be dropped.
Why:
- F3: Among new 30-day lows, a deeper 30-day decline went with a lower excess return over the next 20 days (r = −0.28, n = 61). The correlation was negative in all four coin-by-half subsets: BTC −0.28 and −0.44, ETH −0.07 and −0.32. Across all grid bars the 30-day return had no such link (r = −0.003, n = 179), so the effect is specific to new-low bars.
- F4: The RSI divergence added nothing at lows. Divergence lows averaged −4.4% excess (t = −1.03, n = 28) and non-divergence lows −3.3% (t = −1.12, n = 49), a difference with Welch t = −0.20.
