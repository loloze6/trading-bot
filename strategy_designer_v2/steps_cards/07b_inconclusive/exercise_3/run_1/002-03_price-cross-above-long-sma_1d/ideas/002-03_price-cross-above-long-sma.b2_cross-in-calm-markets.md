---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.b inconclusive
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: After the coin's close has crossed above its long moving average, price keeps rising further than holding the coin over the following bars, only while the coin's recent volatility is low, and the calmer the market, the larger the move that follows.
Consequence: A trader would hold the trend after an upward cross in calm markets and stand aside when volatility is high.
Why:
- F2: The positive mean comes from a few large outcomes, not from a typical drift: the median 20-bar excess on above-SMA bars is −3.6%, only 40.6% of them beat the coin's mean, the skew is 7.4, and the 10 largest cases add up to 5.6 times the total sum of excess returns.
- F6: The effect is drowned by market regimes: above-SMA 20-bar excess is −13.2% in 2018 (t −2.76) and −17.3% in 2022 (t −3.12), and slightly positive (+0.4% to +3.6%) in 2019–2021 and 2023–2025, with every year showing a similar sign for below-SMA bars too.
- F7: Calm conditions favour it: above-SMA bars in the lowest third of 30-bar volatility average +2.3% excess (5%-trimmed +0.9%, t 1.33, n 102), against −1.2% in mid and −0.3% (trimmed −2.8%) in high volatility.
