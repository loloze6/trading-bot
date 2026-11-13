---
brief: 002_moving-average-cross-trend-persistence
source-idea: N4-03_breakouts-pay-in-uptrends
line: 7.d not profitable
backtest: N4-03_breakouts-pay-in-uptrends_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: Below its 200-day average, a coin whose close reaches the top of its 20-day range then rises over the next 10 days more than its usual 10-day move.
Consequence: Refuse shorts at range highs in downtrends, and treat such highs as the start of a rebound.
Why:
- F1: The short side causes most of the book's loss. The 1330 SHORT trades in the mean_reversion regime average −1.58 % before fees, −2104 % summed, and short bars run −0.00103 a day against +0.00102 for long bars. When the short forecast is at its strongest (≤ −10), the coin then beats holding by +0.034 over 10 days (t 1.80, 37 non-overlapping cases). In a downtrend, a close near the 20-day high is followed by a rise, not a fall.
- F3: Every position pays when it points the same way as the past 20-day move. Longs gross +0.0029 a day when the 20-day return is up and −0.00082 when it is down. Shorts gross −0.00225 a day when it is up and +0.00052 when it is down.
