---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal
line: 7.g patterns
backtest: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's 24-hour volatility is low relative to its 30-day volatility, the larger its 1-hour return relative to its 24-hour volatility, the more its return over the next 24 hours continues in the same direction.
Consequence: A trader would follow, not fade, an outsized hourly move that breaks a quiet market, holding it for a day.
Why:
- F4: Across the other 23 hours, the regime set by recent volatility decides the 24-hour direction. Where 24-hour volatility is high against 30-day volatility, hourly moves of 1 to 2 usual moves reverse by +0.22 % (t 5.06, 17453 cases) and moves above 3 by +0.35 % (t 2.32). Where it is low, moves of 2 to 3 continue by -0.18 % (t -2.79) and moves above 3 by -0.43 % (t -3.10, 951 cases).
