---
brief: 010_rsi-midline-regime-direction
source-idea: 010-01_rsi-above-share-continuation.b1_rsi-share-more-coins
line: 7.d not profitable
backtest: 010-01_rsi-above-share-continuation.b1_rsi-share-more-coins_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: Comparing days on which a coin closes on the same side of its 100-day average price, the larger the share of the past 30 days that its 14-day RSI has spent above 50, the lower the coin's return over the next 14 days.
Consequence: A long stay of RSI on one side marks a move that is spent rather than one that continues, so a trader would lean against the stretch within the coin's trend instead of following it.
Why:
- F5: Within each 100-day trend state, the share runs the wrong way. The slope of the 14-day excess return on the forecast has t = -2.51 below the 100-day average and t = -2.02 above it (216 cases each). A longer stay above 50, compared within the same trend, is followed by weaker returns.
- F4: The forecast does not order the next 14 days' returns. The pooled slope has t = -0.30 over 1152 non-overlapping cases. The most negative forecast bucket, (-20, -10], was followed by a mean 14-day return of +3.4 % (n = 320). The most positive bucket, (10, 20], was followed by +1.1 %, with a median of -2.7 % (n = 272).
