---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.d not profitable
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While the close is above its long moving average, price keeps drifting upward, except when the recent rise is already extreme. The more stretched the rise over recent months, the smaller the drift that follows and the larger the falls.
Consequence: A trader would cut the long's size when the coin's recent rise is most stretched, which removes the bars with the largest losses and little gain.
Why:
- F4: Gain is also graded by the 60-bar return, and it is lost at both ends. The weakest quintile of the 60-bar return (below -10%) lost money, at -0.00023 per bar (t -2.11). The middle quintiles (+11% to +49%) earned 0.00263 (t 2.71) and 0.00312 (t 2.47). The most extended quintile (above +49%) earned only 0.00129 (t 0.93), at an allocation of 0.73 and with the largest summed losses of any quintile (-14.1).
- F5: Among high-forecast bars (forecast above 10), the most extended 20-bar rise (above +35%) earned 0.00199 per bar (t 0.89) with the largest summed losses (-11.7). A 20–35% rise earned 0.00676 (t 3.94).
- F1: The Calmar check failed (0.3855 against 0.75) because the book rode the coins' long down legs. Its deepest fall was -43% over 207 days from w15 to w17, while holding the coins fell -44% over the same days. The next falls were -29% (w18–w19, holding -44%), -23% (w21–w22, holding -39%) and -22% (w12–w13, holding -67%).
