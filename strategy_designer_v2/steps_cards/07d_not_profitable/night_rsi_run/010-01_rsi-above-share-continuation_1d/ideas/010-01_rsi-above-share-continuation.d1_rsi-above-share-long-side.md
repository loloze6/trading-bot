---
brief: 010_rsi-midline-regime-direction
source-idea: 010-01_rsi-above-share-continuation
line: 7.d not profitable
backtest: 010-01_rsi-above-share-continuation_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: The larger the share of the past 30 days that a coin's 14-day RSI has spent above its midpoint of 50, the higher the coin's return over the next 14 days, only while that share is above one half.
Consequence: A trader should lean long more heavily the longer RSI has held above 50 and should not short when RSI has mostly sat below 50, since below the midline the signal carries the book's deepest falls and no gain.
Why:
- F1: The book's chained daily returns fall at most -53.0% against a yearly return of 30.6% (Calmar 0.577, below the 0.75 needed), and the deepest fall runs 413 days across w2-w5, where short positions lose a summed -0.554 against -0.132 for long positions.
- F2: Short days barely earn and long days carry the book: long days average +0.00186 per day (n=2793) against +0.00019 on short days (n=2866), and short days average -0.00002 in BTC and +0.00039 in ETH.
- F3: The short side alone has a Sharpe of 0.113, a yearly return of -1.1% and a deepest fall of -67.7%; the long side alone has a Sharpe of 1.024, a yearly return of 31.9% and a deepest fall of only -35.4%, giving a Calmar of 0.902, above the 0.75 rule.
- F4: Almost all of the book's gain is timing rather than the market's own rise: the market part is 0.000033 of a mean daily return of 0.00099, and on long days the coin's 30-day return averages +17.3% against -10.0% on short days.
