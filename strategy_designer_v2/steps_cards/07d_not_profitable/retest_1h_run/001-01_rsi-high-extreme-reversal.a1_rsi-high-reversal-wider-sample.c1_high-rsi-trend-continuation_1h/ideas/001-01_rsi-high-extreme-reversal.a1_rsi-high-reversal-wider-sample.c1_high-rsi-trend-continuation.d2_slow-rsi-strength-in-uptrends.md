---
brief: 001_rsi-extremes-predict-next-move
source-idea: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-trend-continuation
line: 7.d not profitable
backtest: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-trend-continuation_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The higher a coin's 14-day RSI has stood above 50 on average over the past 7 days, the more its price rises above its usual move over the next 10 days, only while its 60-day return is positive.
Consequence: Take RSI-strength longs only in coins whose 60-day trend is up, where the gain clearly beats the fees.
Why:
- F3: The gain sits in the forecast's slow part. Holding the position set at the start of each 168-hour block keeps a gross gain of 0.000822 a day, slightly more than the hourly 0.000774, while fees fall to 0.000040 a day, for a net of +0.000782 a day; 24-hour blocks already net +0.000574 a day.
- F5: The gain is mostly in the trending regime (60-day return positive). It earns 0.000056 an hour gross there, with an average position of 0.37, against 0.000009 an hour with a position of 0.12 in the unknown regime, while fees are similar in both (0.000097 and 0.000086 an hour).
- F7: Every coin loses after fees on hourly trading. Daily gross ranges from -0.00036 to 0.00155 against daily fees of 0.00158 to 0.00341, and XMR has both the highest turnover (0.114 an hour) and a negative gross.
