---
brief: 005_rsi-divergence-predicts-reversal
source-idea: 005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence
line: 7.d not profitable
backtest: 005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin makes a new 30-day low with its 14-day RSI above its reading at the previous low, the coin keeps falling over the next 20 days. The fall is larger the further its close sits below its 100-day average.
Consequence: A divergence low deep under the 100-day average is a reason to refuse a long, or to lean short, for the following weeks.
Why:
- F4: The 20-day rebound is not in the data. On 55 non-overlapping divergence events the mean 20-day return is -1.5%, or -4.1% against the coin's average. The mean 5-day return is +0.86%, so any bounce comes in the first days and is then given back.
- F7: Divergence lows sit inside downtrends, and the deeper the downtrend, the worse the outcome. 53 of 55 events closed below the coin's 100-day average. Their 20-day excess return has Spearman +0.15 with the distance to that average, so further below means a worse 20 days.
- F8: The book's falls come from a few bear windows. The book summed -0.172 in w1 and -0.161 in w24, where the coin summed -0.41 and -0.50.
