---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.g patterns
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's close is very far above its 200-day SMA, more than 60%, and its 20-day volatility is high, the coin's next 20 bars rise less than when it sits moderately above the SMA, by 30 to 60%.
Consequence: A trader would cut or refuse longs once price is stretched far above the long average in high volatility, and keep them in the moderate band.
Why:
- F6: Bars more than 60% above the SMA had a 20-bar return of only +1.3% with a 36.6% hit rate and 6.4% daily volatility, against +5.6% for bars 30–60% above. The book's 1% largest daily losses (mean -22.5%) and gains (mean +27.7%) occurred at average distances of 82% and 141% above the SMA, with 20-day volatility of 0.080 against 0.044 for the average held bar. The large losses followed a -5.7% 5-day move, and the large gains followed a +28% 5-day move.
- F5: Forward 20-bar returns rose with the forecast level, but only at the top. On non-overlapping samples they were -0.36% for forecast 0–5 (t=-0.20, n=111), +1.6% for 5–10, +2.7% for 10–15 and +8.1% for 15–20 (t=1.69, n=113). Flat bars (forecast 0) earned +2.57% (t=2.42, n=412), so being just above the SMA did worse than being below it.
