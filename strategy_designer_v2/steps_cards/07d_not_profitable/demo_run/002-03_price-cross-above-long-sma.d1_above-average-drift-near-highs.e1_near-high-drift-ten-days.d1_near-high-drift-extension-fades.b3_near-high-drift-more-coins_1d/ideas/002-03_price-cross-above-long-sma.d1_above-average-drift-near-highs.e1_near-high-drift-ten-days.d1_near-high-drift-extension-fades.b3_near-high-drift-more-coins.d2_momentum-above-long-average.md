---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades.b3_near-high-drift-more-coins
line: 7.d not profitable
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades.b3_near-high-drift-more-coins_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's close is above its 200-day average, the larger its 30-day return, the larger its rise over the next 10 days.
Consequence: A trader would lean longer into the coins with the strongest 30-day runs above their long average, rather than shorting them as exhausted.
Why:
- F2: Extended runs keep rising rather than fading. On the 513 extended grid cases (ext30 at or below -5, mean 30-day return of 116%), the excess 10-day return was +0.0241 (t 2.63). Within them, the slope of that return on the 30-day return was flat (t -0.01), so the larger extension brings no smaller rise.
- F3: Over the whole trending regime, the 30-day return predicts the next 10 days with a positive slope (t 3.48, 1547 cases). The excess 10-day return rises from -0.031 in the lowest 30-day-return quintile to +0.022 to +0.032 in the top two.
- F5: Because of the penalty, the book is short far more often than long: 10327 short bars against 5802 long, in coins that rose 0.0015 a day. This gives a market part of -0.000048 per bar and a book Sharpe of -0.19, against 0.51 for holding.
