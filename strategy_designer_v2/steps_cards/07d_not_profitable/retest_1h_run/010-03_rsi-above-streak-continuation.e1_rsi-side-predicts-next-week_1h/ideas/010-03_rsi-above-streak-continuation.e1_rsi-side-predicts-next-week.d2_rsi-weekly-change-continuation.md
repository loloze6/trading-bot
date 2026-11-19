---
brief: 010_rsi-midline-regime-direction
source-idea: 010-03_rsi-above-streak-continuation.e1_rsi-side-predicts-next-week
line: 7.d not profitable
backtest: 010-03_rsi-above-streak-continuation.e1_rsi-side-predicts-next-week_1h
instruments: BTC, ETH, BNB
bar: 1h
period: folds A, B, C, D
---
Idea: The more a coin's 14-day RSI has risen over the past 7 days, the higher the coin's return over the next 7 days, and the more it has fallen, the lower that return.
Consequence: A trader would lean with the recent change in RSI rather than its level, held for about a week.
Why:
- F3: The traded forecast is not the RSI's distance from 50. It correlates only 0.35 (BTC) and 0.39 (ETH) with RSI−50 and agrees with its sign on 78% of bars. Once both are scaled, it loads almost as much on RSI's 7-day change (7.9 and 7.8) as on its level (8.5 and 8.9), because the 337-bar standardisation measures RSI against its own 14-day mean.
- F4: The level the idea names carries no 7-day edge. RSI−50 scaled × 168h excess return gives t = −0.98 (n = 718 non-overlapping cases), and its quintiles do not line up: excess +0.0012, −0.0154, +0.0016, +0.0024, −0.0062 from lowest to highest. RSI's 7-day change gives t = +2.01, and the traded forecast t = +1.37.
