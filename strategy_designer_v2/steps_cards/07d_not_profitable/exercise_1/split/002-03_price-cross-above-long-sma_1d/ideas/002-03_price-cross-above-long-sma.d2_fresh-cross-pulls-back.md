---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.d not profitable
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In the first weeks after a coin's close crosses above its 200-day average, the coin's next 20-day return falls below its average return, as the cross is followed by a pullback toward the average.
Consequence: Refuse longs on fresh upward crosses, since they mark noise around the average more than the start of a trend.
Why:
- F5: Losses come from the first weeks of a trend, the noise around the cross.
- F6: Bars 5-20 days into an above-SMA run have negative gross return (-0.00080 per day) and a 20-bar forward return of only 0.75%. Bars 60-120 days in earn 0.0045 per day and 6.0% over 20 bars.
- F7: Profit is concentrated in a few trades. The win rate is 0.30 and the median trade is -3.6%. The top 5% of trades sum to +15845%, more than the total of +9433%, while losers sum to -12235%.
