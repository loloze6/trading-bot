---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.g patterns
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's 20-day volatility is in its lowest range, the coin rises further over the next 20 bars than when its volatility is higher.
Consequence: A trader would favour holding longs through calm stretches and expect less 20-bar gain from turbulent ones.
Why:
- F9: Higher 20-day volatility came with higher next-day returns: they rose monotonically from +0.01% in the lowest volatility quintile to +0.29% in the highest. Forward 20-bar returns ran the other way, highest in the calmest quintile at +5.9%, against +1.6% to +3.6% in the others.
