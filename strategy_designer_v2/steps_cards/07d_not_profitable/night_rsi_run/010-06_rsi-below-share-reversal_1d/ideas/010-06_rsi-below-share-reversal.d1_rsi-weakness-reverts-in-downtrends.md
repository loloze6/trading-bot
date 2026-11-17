---
brief: 010_rsi-midline-regime-direction
source-idea: 010-06_rsi-below-share-reversal
line: 7.d not profitable
backtest: 010-06_rsi-below-share-reversal_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: The larger the share of the past 30 days that a coin's 14-day RSI has spent below 50, the higher the coin's return over the next 14 days, only while the coin's 60-day return is negative.
Consequence: A trader would buy RSI-weak coins in proportion to how long they have sat below the midpoint, but only inside a falling 60-day trend, and would not short RSI-strong coins in rising markets.
Why:
- F2: Most of the loss comes from going short while the coin's 60-day return was positive (the RSI below-share is low then): on those 1308 days the book's mean daily gain was -0.00255 and its timing -0.00157, while long days in falling markets (1141 days) also lost, at a timing of -0.00158.
- F3: The share of days with RSI below 50 is mostly a mirror of the past trend, correlating -0.80 with the 60-day return and -0.73 with the 30-day return, and the pooled slope of the next 14-day return on the forecast is -0.00118 (t -1.65, 373 cases), negative for both BTC (t -1.28) and ETH (t -1.09).
- F4: The reversal the idea bets on appears only when the coin's 60-day return is negative: there the slope of the coin-demeaned next 14-day return on the share is +0.234 (t 2.27, n 65), and the forecast's slope is +0.0047 (t 1.51, n 64), and on days the book was short in a falling market its timing was +0.00154 (194 days).
