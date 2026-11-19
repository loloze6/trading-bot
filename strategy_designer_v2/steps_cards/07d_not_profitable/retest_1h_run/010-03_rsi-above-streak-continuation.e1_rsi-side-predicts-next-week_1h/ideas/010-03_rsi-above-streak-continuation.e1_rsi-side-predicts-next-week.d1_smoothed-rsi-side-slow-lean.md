---
brief: 010_rsi-midline-regime-direction
source-idea: 010-03_rsi-above-streak-continuation.e1_rsi-side-predicts-next-week
line: 7.d not profitable
backtest: 010-03_rsi-above-streak-continuation.e1_rsi-side-predicts-next-week_1h
instruments: BTC, ETH, BNB
bar: 1h
period: folds A, B, C, D
---
Idea: The higher a coin's 14-day RSI sits above 50 at the close, the higher its return over the next 1 to 7 days, and the lower it sits below 50, the lower that return, with the distance read as its average over the past 3 days, so the move follows RSI's slow drift rather than its hour-to-hour swings around 50.
Consequence: A trader would lean toward RSI's side only as its smoothed distance from 50 builds and would rarely flip, which keeps fees well below the gain the lean collects.
Why:
- F1: Fees eat the gain: gross gain per bar is +0.000065 (BTC) and +0.000083 (ETH), but fees are 0.000171 and 0.000152 per bar, so the book loses -0.0025 and -0.0017 per day while holding the coins makes +0.0012 and +0.0014 per day.
- F2: The position churns. It turns over 0.23 (BTC) and 0.17 (ETH) of the book per bar and trades on 51% of bars, and 31–34% of that turnover comes from sign flips. The forecast changes sign 2.4–2.6 times a day even though its 24-hour autocorrelation is 0.73.
- F3: The traded forecast is not the RSI's distance from 50. It correlates only 0.35 (BTC) and 0.39 (ETH) with RSI−50 and agrees with its sign on 78% of bars. Once both are scaled, it loads almost as much on RSI's 7-day change (7.9 and 7.8) as on its level (8.5 and 8.9), because the 337-bar standardisation measures RSI against its own 14-day mean.
