---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-04_price-cross-below-long-sma
line: 7.b inconclusive
backtest: 002-04_price-cross-below-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's close has stayed below its 200-day SMA for roughly two to five months without interruption, the coin keeps falling over the next 10 days, by more than its usual drift and more than the six-coin market.
Consequence: A trader would short a coin below its 200-day average only once it has been below for about two months, and skip shorts in the first weeks after the cross.
Why:
- F7: The effect leans toward long stays below the average. Blocks 61–150 days into a run below the SMA200 gain +0.017 (t = 1.81, hit 55%, n = 210), against -0.004 (t = -0.37, n = 283) in the first 20 days and -0.002 (t = -0.32) at 21–60 days. The 61–150-day gain stays positive net of the market (+0.006, t = 1.49).
- F1: Over the 930 non-overlapping 10-bar blocks with a short position, the mean excess short gain is +0.0007 per block against a block standard deviation of 0.140 (t = 0.16, hit rate 52.5%), so the effect is roughly 1/200 of the noise; the pooled main measure is -0.0007 (t = -0.27).
