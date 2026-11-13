---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-04_price-cross-below-long-sma
line: 7.g patterns
backtest: 002-04_price-cross-below-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin below its 200-day average has fallen 30% or more over the past 30 days, it tends to rise over the next 10 bars.
Consequence: A trader would take a long after a 30-day crash below the long average, rather than add to a short.
Why:
- F2: Below the SMA200, a 30-day crash leads to a rebound. Bars whose past-30-day return is ≤ -30% are followed by +2.87% over 10 bars (t 4.48, 58% up), against +0.22% to +1.20% for the milder below-SMA buckets.
- F1: The deepest short zone does not continue falling, it rebounds. Bars with forecast ≤ -15 are followed by a mean 10-bar coin return of +3.57% (t 7.73, 59.5% up) and a next-day return of +0.45% (t 3.24). That is more than the +1.58% after flat bars (forecast 0, t 7.72), and the short book is positioned against this rebound.
