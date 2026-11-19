---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods
line: 7.d not profitable
backtest: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: Over the next 24 hours, a coin rises after a fall over its last 24 hours, and the larger that fall relative to the coin's usual 24-hour volatility, the larger the rise, more strongly when the coin's 24-hour volatility is high relative to its 30-day average.
Consequence: A trader would buy coins after unusually large one-day falls in volatile periods and hold for a day, refusing the trade when the rebound does not appear.
Why:
- F4: Faded over the next 24 hours, a large past move pays more than a fee, mostly when 24h volatility is high:
- F5: Volatility carries the gain: per-bar gross rises from -0.000006 in the lowest fifth of 24h vol relative to its 30-day average to 0.000283 in the highest fifth.
- F6: The reversal is graded and lopsided toward falls.
