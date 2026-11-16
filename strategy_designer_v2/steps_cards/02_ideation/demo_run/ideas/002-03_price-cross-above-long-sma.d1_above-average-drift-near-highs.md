---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.d not profitable
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While the close is above its long moving average, price keeps drifting upward, and the drift is larger the closer the close sits to its recent high and the stronger its recent rise. The drift fades as the close falls back from its recent high while still above the long average.
Consequence: A trader would scale the long down as the coin pulls back from its recent high. The book would then be mostly out of the coin before the long down legs that make its deepest falls.
Why:
- F1: The Calmar check failed (0.3855 against 0.75) because the book rode the coins' long down legs. Its deepest fall was -43% over 207 days from w15 to w17, while holding the coins fell -44% over the same days. The next falls were -29% (w18–w19, holding -44%), -23% (w21–w22, holding -39%) and -22% (w12–w13, holding -67%).
- F2: The book's gain comes only from bars where the coin is still rising and near its recent high. Active bars with a non-negative 20-bar return and a close within 15% of the 60-bar high earned a mean 0.00170 per bar (t 3.38, n 5246). Active bars with a negative 20-bar return and a close still within 15% of the high earned 0.00002 (t 0.03, n 1165), yet the book held a mean allocation of 0.52 there and lost a summed -6.18 on the down days. With a negative 20-bar return and a deep pullback, the gain was 0.00025 (t 0.95, n 2229).
- F3: Gain is graded by distance from the 60-bar high. Active bars within 2% of it earned 0.00270 per bar (t 2.39) at an allocation of 0.86. Bars 7–14% below it earned 0.00017 (t 0.25) at an allocation of 0.49. Bars more than 25% below it earned 0.00007 (t 0.27).
- F4: Gain is also graded by the 60-bar return, and it is lost at both ends. The weakest quintile of the 60-bar return (below -10%) lost money, at -0.00023 per bar (t -2.11). The middle quintiles (+11% to +49%) earned 0.00263 (t 2.71) and 0.00312 (t 2.47). The most extended quintile (above +49%) earned only 0.00129 (t 0.93), at an allocation of 0.73 and with the largest summed losses of any quintile (-14.1).
