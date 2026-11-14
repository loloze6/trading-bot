---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.b inconclusive
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's close is above its 200-day SMA and its percent distance above the SMA is larger than it was 10 bars earlier, its return over the next 20 bars beats its own average drift.
Consequence: A trader would hold the long only while the gap above the average is widening, and stand aside when the gap is shrinking.
Why:
- F3: The same split appears with the distance to the SMA: when the distance has risen over the last 10 bars, excess is +0.039 (t 6.93, hit 46.5%, n 3494), and when it has fallen it is -0.025 (t -5.72, hit 37.6%, n 3552).
- F2: Within forecast>0 bars, the effect splits by recent momentum: when the close is up over the past 20 bars, the 20-bar excess return is +0.035 (t 6.66, hit 45.7%, n 3856), and when it is down it is -0.027 (t -5.93, hit 37.5%, n 3190); the t-values use overlapping bars, so they are overstated.
- F9: The positive means come from right-skewed returns, not from frequent wins: active bars have mean excess +0.0065 against +0.0002 for inactive bars, yet only 42.0% of active bars beat the coin's drift, so most of the time the position is drowned by the coin's own moves.
