---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-04_price-cross-below-long-sma
line: 7.g patterns
backtest: 002-04_price-cross-below-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's close is above its 200-day average and its past-30-day return is between -30% and -15%, it tends to keep falling over the next 10 bars.
Consequence: A trader would short pullbacks of this size that happen above the long average, where the tested book stays flat.
Why:
- F4: Above the SMA200, a pullback leads to further falls. Bars with a past-30-day return between -30% and -15% are followed by -3.94% over 10 bars (t -4.40, 38.7% up). This is the only clearly negative forward pocket found, and it lies where the book is flat.
