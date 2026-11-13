---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-04_price-cross-below-long-sma
line: 7.b inconclusive
backtest: 002-04_price-cross-below-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's close is below its 200-day average and that average has itself been falling steeply over the past few weeks, the coin keeps falling over the next 10 days by more than its usual drift.
Consequence: A trader would take shorts below the long average only when the average is already turning down hard, and refuse them when the average is flat or rising.
Why:
- F5: Shorts gained most when the 200-day average itself had fallen more than 5% over the prior 20 bars: +1.6% excess fall (t 1.74, hit 54.8%, n 217), against roughly 0% where the average was flat or rising (−0.58% to +0.44%, all |t| < 0.7).
- F1: Across the 930 short blocks the mean excess fall is only 0.07% per 10 bars (t 0.16, hit rate 52.5%), against a block-to-block spread of 14.0%, so any edge is buried in the market's own 10-day moves.
- F4: Sitting deeper below the average does not help: the deepest forecast bucket (−20 to −10) gives −0.15% (t −0.17, n 294), the −10 to −5 bucket gives +0.64% (t 0.76), and the slope of excess return on allocation has the wrong sign (−0.0056).
