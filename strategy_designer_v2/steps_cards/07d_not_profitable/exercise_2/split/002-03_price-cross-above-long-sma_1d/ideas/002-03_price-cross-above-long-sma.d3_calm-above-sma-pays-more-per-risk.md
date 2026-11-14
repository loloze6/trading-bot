---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.d not profitable
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin is above its 200-day SMA, its forward 20-bar return per unit of its own 20-day volatility is higher when that volatility is below the coin's usual level than when it is above.
Consequence: Shrink the long position when 20-day volatility is high rather than adding to it, so the most leveraged days stop producing the drawdowns that sink Calmar.
Why:
- F1: The losses that sink Calmar come from the most leveraged bars: the worst 5% of book days (852 days) held a mean allocation of 1.66, with 89% of them above 1.0 and 48% at the forecast cap of 20, and they summed to -99.0 in daily return units against a book total of +17.4.
- F2: At the forecast cap the book holds about twice its capital (mean allocation 1.96) in the coins' most volatile state, with 20-day volatility of 0.056 against 0.040–0.044 elsewhere and a daily return std of 634 bp against 441–471 bp in the buckets from 0 to 15, so the daily Sharpe of the cap bucket (0.051) is below that of the 10–15 bucket (0.063).
- F12: Per window, the book's worst drawdown (-89.5%) is deeper than holding's (-77.0%), even though its mean drawdown is shallower (-29.2% against -39.0%), and window returns track holding with a correlation of 0.88.
