---
brief: 001_rsi-extremes-predict-next-move
source-idea: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample
line: 7.c rejected
backtest: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's 60-day return is positive, the higher its 14-day RSI, the more the coin rises over the next 10 days, by more than its usual 10-day move.
Consequence: A trader should refuse to short overbought readings in an uptrend and can lean long, in proportion to RSI strength, for about ten days.
Why:
- F1: The tested short was rejected because price rose more than usual after extreme high RSI: the 595 extreme cases (forecast ≤ -5) on the 5-bar grid had a pooled mean 5-bar excess return of +1.44% (t = +2.58). Only 1 of 6 coins had a negative mean, and the book lost money (Sharpe -1.26, mean daily return -0.075%, of which -0.056% was timing and -0.019% was the market's own drift).
- F2: The rise after high RSI holds where the coin's 60-day return is positive. With 60-day return above 0 and RSI 70–100, the mean excess return was +2.69% over 5 days (n = 112, t = 2.04) and +6.02% over 10 days (n = 61, t = 2.37). In that up-regime, RSI's rank correlation with the 10-day excess return was +0.118 (n = 423, p = 0.015), against -0.020 (n = 404, p = 0.68) when the 60-day return was negative.
- F3: The continuation grows with RSI across all coins. The mean 5-day excess return by RSI bucket rises from -0.96% at RSI 40–50 (n = 833, t = -3.11) to +0.69% at 70–80 (n = 193) and +3.10% at 80–100 (n = 64, t = 1.59). The 10-day figures rise from -1.55% (t = -2.30) to +2.65% and +10.3%.
- F4: Among extreme cases, the 60-day uptrend carries the sample: 268 of 300 had a positive 60-day return, with a mean of +1.91% (t = 2.40). The 32 downtrend cases averaged +1.55% (t = 0.68).
