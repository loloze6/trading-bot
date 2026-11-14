---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.d not profitable
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's close sits above its long moving average, the coin keeps rising in proportion to how far above it the close sits, only while the coin's own recent return over the past several weeks is positive; the more it has risen over those weeks, the larger the further rise.
Consequence: A trader would hold a coin that sits above its long average only while its recent weeks are rising, sized by that rise, and step out when it trades above the average but is falling, which removes the losing long days that made the book's deepest fall.
Why:
- F1: The book's deepest fall was -83% (Calmar 0.14), running from w12 through w21 over 1,051 days; the book summed -0.870 in daily returns while holding the coins summed +0.505. Windows w12, w13, w16 and w18 alone summed -0.342, -0.299, -0.199 and -0.493, against holding's -0.027, -0.125, +0.544 and +0.013.
- F2: While long, the position's daily gain rose steadily with the coin's past 20-bar return. By quartile of that return (2,035 bars each) the mean daily gain was -0.00034 (t -0.41), 0.00087 (t 1.04), 0.00196 (t 1.64) and 0.00691 (t 3.04). The top quartile alone carried 14.07 of the summed gain of 19.12.
- F3: While long, the bottom quartile of the past 60-bar return (mean -23%, n 1,267) lost -0.00070 a day (t -2.78). Every other quartile gained between 0.0025 and 0.0042 a day.
- F4: Long days with a negative past 20-bar return earned nothing: -0.00049 a day (n 3,145) when more than 10% below the 60-bar high, and -0.00042 (n 1,568) when near it. Long days with a positive past 20-bar return earned 0.0037 (t 2.06) and 0.0043 (t 3.08).
- F5: In the four losing windows the book was long mostly on falling coins. The median past 60-bar return was -8.2% against +20.8% elsewhere, and the median fall from the 60-bar high was -22% against -8%. There, long days with a negative past 20-bar return lost -0.0066 a day (t -2.82, n 932), while those with a positive one lost only -0.0016 (t -0.82, n 671).
