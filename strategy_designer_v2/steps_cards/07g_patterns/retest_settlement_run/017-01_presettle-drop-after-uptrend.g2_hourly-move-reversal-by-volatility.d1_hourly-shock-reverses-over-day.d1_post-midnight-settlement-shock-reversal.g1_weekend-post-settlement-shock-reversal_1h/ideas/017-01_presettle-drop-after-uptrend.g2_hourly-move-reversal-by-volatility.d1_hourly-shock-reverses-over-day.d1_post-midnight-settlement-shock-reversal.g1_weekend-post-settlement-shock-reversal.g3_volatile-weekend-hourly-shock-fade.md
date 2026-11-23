---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g1_weekend-post-settlement-shock-reversal
line: 7.g patterns
backtest: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g1_weekend-post-settlement-shock-reversal_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: On a Saturday or Sunday, the larger a coin's 1-hour return relative to its 24-hour volatility, the more its next 24 hours run the opposite way, and the reversal is larger the higher the coin's 24-hour volatility stands against its 30-day volatility.
Consequence: A trader would fade weekend hourly shocks hardest when the coin is unusually volatile, and lightly when it is calm.
Why:
- F5: The tested 1-hour fade is not special to the 00:00 hour on weekends. Weekend 1-hour moves are followed by a 24-hour reversal at 18 of 24 hours of the day (12:00 +20.5 bp, t 3.15; 18:00 +23.8 bp, t 3.32; 20:00 +26.1 bp, t 3.85). On weekdays only 11 of 24 hours are positive, and several are negative with t below −2.5 (03:00, 06:00, 07:00).
- F6: The weekend fade is larger when 24-hour volatility is high against its 30-day level: +23.1 bp (t 6.3) in the top third against +5.3 bp (t 3.2) in the bottom third. On weekdays the same split runs from +7.4 bp (t 4.2) to −10.8 bp (t −6.4). These counts use overlapping returns, so the t values are inflated.
