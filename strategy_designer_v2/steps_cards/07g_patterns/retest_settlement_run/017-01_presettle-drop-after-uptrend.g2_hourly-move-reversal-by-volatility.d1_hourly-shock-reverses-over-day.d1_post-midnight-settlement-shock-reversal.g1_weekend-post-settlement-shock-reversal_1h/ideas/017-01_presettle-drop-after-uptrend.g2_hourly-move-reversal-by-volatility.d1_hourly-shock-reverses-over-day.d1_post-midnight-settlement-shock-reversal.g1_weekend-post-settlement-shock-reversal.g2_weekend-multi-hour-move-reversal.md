---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g1_weekend-post-settlement-shock-reversal
line: 7.g patterns
backtest: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g1_weekend-post-settlement-shock-reversal_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: On a Saturday or Sunday, the larger a coin's 4-hour to 12-hour return at any hour of the day, relative to its 24-hour volatility, the more its return over the next 24 hours reverses it.
Consequence: A trader would treat weekend moves of several hours as flow that will reverse, and fade them through the weekend rather than only after midnight.
Why:
- F4: The same fade at other weekend anchor hours is weaker but has the same sign. At 16:00 the 12-hour fade gives +29.6 bp (t 4.07) and the 4-hour fade +21.4 bp (t 3.25). At 04:00 the 12-hour fade gives +35.5 bp (t 4.69). At the same anchors on weekdays, every slope is between −14.5 and +0.5 bp.
- F5: The tested 1-hour fade is not special to the 00:00 hour on weekends. Weekend 1-hour moves are followed by a 24-hour reversal at 18 of 24 hours of the day (12:00 +20.5 bp, t 3.15; 18:00 +23.8 bp, t 3.32; 20:00 +26.1 bp, t 3.85). On weekdays only 11 of 24 hours are positive, and several are negative with t below −2.5 (03:00, 06:00, 07:00).
