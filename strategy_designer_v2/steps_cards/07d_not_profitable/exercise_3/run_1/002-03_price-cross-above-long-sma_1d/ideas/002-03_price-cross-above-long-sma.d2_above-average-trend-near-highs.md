---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.d not profitable
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's close sits above its long moving average, the coin keeps rising in proportion to how far above it the close sits, except when the close has fallen far below its recent high, in which case the deeper that fall, the weaker the rise that follows.
Consequence: A trader would cut a long on a coin above its long average as the coin falls from its recent high, so the book is not long through the drawdowns that carried its losing windows.
Why:
- F1: The book's deepest fall was -83% (Calmar 0.14), running from w12 through w21 over 1,051 days; the book summed -0.870 in daily returns while holding the coins summed +0.505. Windows w12, w13, w16 and w18 alone summed -0.342, -0.299, -0.199 and -0.493, against holding's -0.027, -0.125, +0.544 and +0.013.
- F3: While long, the bottom quartile of the past 60-bar return (mean -23%, n 1,267) lost -0.00070 a day (t -2.78). Every other quartile gained between 0.0025 and 0.0042 a day.
- F5: In the four losing windows the book was long mostly on falling coins. The median past 60-bar return was -8.2% against +20.8% elsewhere, and the median fall from the 60-bar high was -22% against -8%. There, long days with a negative past 20-bar return lost -0.0066 a day (t -2.82, n 932), while those with a positive one lost only -0.0016 (t -0.82, n 671).
