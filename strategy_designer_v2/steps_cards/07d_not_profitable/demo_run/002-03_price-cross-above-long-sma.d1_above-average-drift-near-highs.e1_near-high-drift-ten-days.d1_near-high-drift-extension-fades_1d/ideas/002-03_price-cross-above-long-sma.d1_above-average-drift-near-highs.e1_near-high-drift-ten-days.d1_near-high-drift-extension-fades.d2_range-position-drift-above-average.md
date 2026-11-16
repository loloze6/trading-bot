---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades
line: 7.d not profitable
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's close is above its 200-day average, the higher its close sits in its 20-day close range, the larger its rise over the next 10 days.
Consequence: A trader would size longs above the long average by how near the close is to its 20-day high, and would not short a coin that sits low in its range there.
Why:
- F3: The tested situation itself carries the effect. On the 10-day grid of trending bars, the forward 10-day return minus the coin's mean rises with range position: raw range slope t 3.45 (n 698), range20 slope t 3.08 (n 833). The top range20 quintile averages +0.0477 and the bottom -0.0212. By raw range, the top quintile averages +0.0668 against -0.0162 for the bottom.
- F5: Removing the penalty turns the book positive. On trending bars, a position of 2 × (raw range position - 0.5) gives a mean of +0.000647 a day and a Sharpe of 0.81 before fees, against the book's -0.000361 and -0.42. The book's long bars alone give a Sharpe of 0.51.
