---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.b inconclusive
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's daily close is above its 200-day SMA and also higher than it was 20 bars earlier, its return over the next 20 bars beats its own average drift.
Consequence: A trader would take the above-average long only when the coin's 20-bar momentum is also up, and refuse it when the coin has been falling while still above the average.
Why:
- F2: Within forecast>0 bars, the effect splits by recent momentum: when the close is up over the past 20 bars, the 20-bar excess return is +0.035 (t 6.66, hit 45.7%, n 3856), and when it is down it is -0.027 (t -5.93, hit 37.5%, n 3190); the t-values use overlapping bars, so they are overstated.
- F9: The positive means come from right-skewed returns, not from frequent wins: active bars have mean excess +0.0065 against +0.0002 for inactive bars, yet only 42.0% of active bars beat the coin's drift, so most of the time the position is drowned by the coin's own moves.
- F1: The block result rests on a few outliers: the 499 active blocks have mean 0.340, median -0.178, std 6.08 and max 77.5; the top 10 blocks hold 183% of the total; after a 1% winsorisation t falls from 1.25 to 0.60; and dropping the top 5 blocks turns the mean negative (-0.122, t -0.74), with only 37% of blocks positive.
