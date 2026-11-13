---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.g patterns
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: Once a coin's close moves above its 200-day SMA, it usually falls back below within a few days, and only a minority of these moves become long runs above the average.
Consequence: A trader could refuse to treat a fresh close above the long average as an entry until it has held there for some days.
Why:
- F1: Over 783 trades, those held 5 days or less lost on average (−6.2% net, 1.2% winners, for 244 trades of ≤1.5 days; −6.5% net, 6.7% winners, for 539 trades of 1.5–5 days), while the 204 trades held over 60 days made +60.7% net with 75% winners, so the book's gain comes from a few long holds and short stays above the average are mostly whipsaws.
