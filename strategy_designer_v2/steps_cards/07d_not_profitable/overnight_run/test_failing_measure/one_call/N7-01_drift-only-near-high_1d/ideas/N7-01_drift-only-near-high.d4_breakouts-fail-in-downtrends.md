---
brief: 002_moving-average-cross-trend-persistence
source-idea: N7-01_drift-only-near-high
line: 7.d not profitable
backtest: N7-01_drift-only-near-high_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose longer trend is falling (close below a long moving average), new 20-day closing highs are followed by below-average returns: they are failed bounces, not new trends.
Consequence: Refuse breakout longs while the coin's longer trend points down, avoiding the down-market windows where the book lost more than holding.
Why:
- F6: In several falling windows the book lost more than simply holding the coins, which points to failed breakouts in down markets.
- F1: The Calmar failure comes from deep falls inside single windows, not from one bad stretch. The book's largest falls within a window were −33.4% (w10), −31.6% (w13), −30.7% (w22), −30.3% (w12) and −29.8% (w7), against a 10-day block mean of +1.36%. Across the 304 non-overlapping 10-day blocks of the book's daily returns, the worst was −18.4%, and the worst 10% of blocks hold 54% of all losses.
