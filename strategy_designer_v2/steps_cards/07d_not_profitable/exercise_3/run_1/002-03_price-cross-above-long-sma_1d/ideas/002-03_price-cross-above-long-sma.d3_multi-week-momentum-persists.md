---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.d not profitable
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: (new idea) A coin's return over the following weeks grows with its own return over the past several weeks, whatever the coin's position against its long moving average, so the stronger the recent rise, the larger the further rise.
Consequence: A trader would size a long by the coin's recent multi-week return rather than by its distance from the long average, staying in rising coins that the long average leaves flat.
Why:
- F2: While long, the position's daily gain rose steadily with the coin's past 20-bar return. By quartile of that return (2,035 bars each) the mean daily gain was -0.00034 (t -0.41), 0.00087 (t 1.04), 0.00196 (t 1.64) and 0.00691 (t 3.04). The top quartile alone carried 14.07 of the summed gain of 19.12.
- F6: The forecast's own grading adds little. By quartile of the raw distance above the 200-day average, the long daily gain moved from 0.00027 (t 1.38) to 0.0045 (t 1.89). In the 20-bar test, the forecast 0-5 and 5-10 buckets had excess returns of -0.029 and -0.011, and only 42% of active bars beat holding.
- F7: The book was long on 56% of days, and the coin rose 0.00087 a day on the days it stood flat. Being out of the market therefore cost the book about as much as holding earned, which pushed its Sharpe 0.065 below holding's.
