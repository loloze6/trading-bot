---
brief: 010_rsi-midline-regime-direction
source-idea: 010-01_rsi-above-share-continuation.b1_rsi-share-more-coins
line: 7.b inconclusive
backtest: 010-01_rsi-above-share-continuation.b1_rsi-share-more-coins_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's own 60-day return is negative, the smaller the share of the past 30 days that its 14-day RSI has spent above 50, the higher the coin's return over the next 14 days.
Consequence: In a coin already falling over 60 days, a long stretch of RSI below its midpoint marks sellers who are exhausted rather than in control, a reason to expect a rebound and to refuse a trend-following short.
Why:
- F2: Across quintiles of the raw share at 14 days the excess return does not rise. The lowest-share quintile (raw -0.46) has the highest excess return, +2.0%, and the highest-share quintile (raw +0.43) has -0.6%; at 30 days the same quintiles show +3.0% and -3.3%.
- F4: When the coin's own 60-day return is negative, the slope on the raw share is clearly negative: t = -3.52 at 14 days (n=211) and t = -2.40 at 7 days (n=566). The same slope while the 60-day return is positive is weaker, at t = -1.40 (n=221).
- F5: The reversal inside 60-day downtrends holds in all six coins, with 14-day slopes of t -2.69 for BTC, -2.17 for ZEC, -1.68 for XMR, -1.08 for LTC, -1.00 for ETH and -0.86 for XRP. It holds without XRP (t = -3.51, n=177). It is strongest in 2018 (t -4.02), 2020 (t -2.87) and 2022 (t -2.94), and it turns positive in 2019 (t +1.54).
- F6: Inside 60-day downtrends the gain sits mostly in the deepest cases. The quartile with the smallest RSI-above share (raw -0.49, 30-day return -26%) earns +12.7% excess over the next 14 days, against -3.9%, -5.0% and -4.2% in the other three quartiles. Only 37.5% of the 14-day cases have a 60-day return inside their window (432 of 1152).
