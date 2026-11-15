---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.g patterns
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 20-day volatility of daily returns is low, a day's return that is large relative to that volatility is followed by a move the same way over the next 5 days. The larger the scaled move, the larger the follow-through, and the effect weakens or reverses as the 20-day volatility rises.
Consequence: A trader would follow a strong day in a calm market and stay out of following strong days in a volatile one.
Why:
- F3: Volatility changes how a day's move carries into the next 5 days. A day's return scaled by its 20-day volatility has a Spearman correlation with the next 5-day excess return of +0.093 in the lowest volatility tercile (n 929, about t 2.8) and −0.057 in the highest (n 929, about t −1.7), a gap of about 3.2 in Fisher z.
- F4: Pooled over all volatility, the scaled 1-day move rises roughly in order into the next 5-day excess return, from −0.0063 at −1.5 to −0.5 to +0.0159 above +1.5 (t 1.67, n 181). The per-coin Spearman correlations range only from −0.021 to +0.071, so the pooled slope is weak.
