---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g2_high-volatility-hourly-shock-reversal
line: 7.g patterns
backtest: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g2_high-volatility-hourly-shock-reversal_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's 24-hour drop relative to its 30-day hourly volatility, the larger its rise over the next 24 hours.
Consequence: A trader would buy a coin after a sharp one-day fall for a one-day rebound, the side of the reversal that carries most of its size.
Why:
- F5: The reversal is larger after drops than after rises. With |z24| > 1, a 24-hour drop is followed by a +0.84 % excess rebound over 24 hours (t 5.7, n 1774), against a +0.30 % excess pullback after a rise (t 2.5, n 1929).
- F1: A coin's 24-hour return, scaled by its 30-day hourly volatility (z24), is followed by a graded reversal over the next 24 hours. On a non-overlapping 24-bar grid, the excess return in the fade direction is -0.06 % (t -1.2, n 7793) for |z24| ≤ 0.5, +0.07 % (t 0.9, n 4287) for 0.5–1, +0.46 % (t 4.7, n 2882) for 1–2, +0.61 % (t 2.2, n 602) for 2–3 and +1.73 % (t 3.1, n 219) above 3, and the pooled slope of the excess 24-hour return on z24 is -0.28 % per unit (t -6.9, n 15806).
- F7: The book's losses come from shorts held long. Short trades average -3.53 % before fees (5182 trades, 38 % winners) against +0.92 % for longs, and shorts held over 168 hours average -18.6 % (n 540). The book loses in 6 of 8 years, including -0.30 % a day in 2020 while the coins rose +0.42 % a day.
