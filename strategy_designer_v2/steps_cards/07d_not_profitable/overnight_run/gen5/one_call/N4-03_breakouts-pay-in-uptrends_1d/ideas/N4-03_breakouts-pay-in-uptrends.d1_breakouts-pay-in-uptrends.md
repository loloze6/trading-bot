---
brief: 002_moving-average-cross-trend-persistence
source-idea: N4-03_breakouts-pay-in-uptrends
line: 7.d not profitable
backtest: N4-03_breakouts-pay-in-uptrends_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A close at or very near its 20-day high, while the coin is above its 200-day average and its 60-day return is positive, is followed by a 10-day rise larger than the coin's usual 10-day move.
Consequence: Take the long only at near-high closes inside an established 60-day uptrend, and drop the short side altogether.
Why:
- F1: The short side causes most of the book's loss. The 1330 SHORT trades in the mean_reversion regime average −1.58 % before fees, −2104 % summed, and short bars run −0.00103 a day against +0.00102 for long bars. When the short forecast is at its strongest (≤ −10), the coin then beats holding by +0.034 over 10 days (t 1.80, 37 non-overlapping cases). In a downtrend, a close near the 20-day high is followed by a rise, not a fall.
- F2: Long trades pay only when the 60-day trend is up. In the trending regime, forecast-active bars beat holding over 10 days by +0.0276 when the past 60-day return is positive (t 2.19, 253 cases), and by −0.0029 when it is negative (t −0.25, 288 cases).
- F3: Every position pays when it points the same way as the past 20-day move. Longs gross +0.0029 a day when the 20-day return is up and −0.00082 when it is down. Shorts gross −0.00225 a day when it is up and +0.00052 when it is down.
- F5: Only the largest forecast earns. Long bars with forecast ≥ 10 beat holding by +0.084 over 10 days (t 2.90, 87 cases). The 2–10 bucket earns +0.005 (t 0.39, 225 cases) and the 0–2 bucket −0.013 (t −1.20, 198 cases). Over all trending grid bars, the regime alone earns +0.0023 (t 0.38, 902 cases).
