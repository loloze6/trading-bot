---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.d2_convex-post-settlement-shock-reversal
line: 7.b inconclusive
backtest: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.d2_convex-post-settlement-shock-reversal_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's percentage return in the first hour after the 00:00 UTC funding settlement, the more its return over the next 24 hours runs the opposite way.
Consequence: A trader would size the daily post-settlement fade on the hour's raw percentage move, taking larger fades on the coins and days whose post-settlement hour moves most in price terms.
Why:
- F5: The effect belongs to the post-settlement hour, not to every hour. The 24-hour faded return is 0.30 % (t 7.73) after the 00:00 bar. After the other 23 hours it lies between −0.12 % and +0.10 %, with no hour above t 2.63.
- F6: The effect is broad:
- F7: The unscaled percentage move of that hour predicts the next 24 hours better than the volatility-scaled one: slope t −11.62 with r² 0.0078, against t −7.84 with r² 0.0036 for the scaled move. The test's measured size, 0.37 % per case or 1.9 times the 0.19 % cost of a trade, leaves room for a better-graded version.
