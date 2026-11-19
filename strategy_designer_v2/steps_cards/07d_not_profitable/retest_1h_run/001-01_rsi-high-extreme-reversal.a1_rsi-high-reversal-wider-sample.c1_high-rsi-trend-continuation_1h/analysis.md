---
line: 7.d not profitable
backtest: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-trend-continuation_1h
idea tested: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-trend-continuation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3044 USD
---
## Findings
- **F1:** Fees eat the book's gain: on hourly positions it earns 0.000774 a day before costs but pays 0.002222 a day in fees (about 0.0011 per unit of turnover), leaving -0.001448 a day, which matches the book's recorded mean daily return of -0.001441 and its Sharpe of -2.07.
- **F2:** The fees come from churn, not from the forecast's size: the forecast changes by 1.88 points per hour on average, switches between flat and long about 3.0 times a day, and the median trade lasts only 2–3 hours, giving 14,000–21,000 trades per coin.
- **F3:** The gain sits in the forecast's slow part. Holding the position set at the start of each 168-hour block keeps a gross gain of 0.000822 a day, slightly more than the hourly 0.000774, while fees fall to 0.000040 a day, for a net of +0.000782 a day; 24-hour blocks already net +0.000574 a day.
- **F4:** Slowed to 168-hour blocks, the book nets a positive sum in 14 of 24 windows, against only 4 of 24 (w11, w15, w16, w17) for the hourly book, so the gain no longer rests on a few periods.
- **F5:** The gain is mostly in the trending regime (60-day return positive). It earns 0.000056 an hour gross there, with an average position of 0.37, against 0.000009 an hour with a position of 0.12 in the unknown regime, while fees are similar in both (0.000097 and 0.000086 an hour).
- **F6:** Of the gross gain, 1.77e-5 an hour is timing and 1.46e-5 an hour is the coins' own rise, so the RSI forecast does carry information beyond being long.
- **F7:** Every coin loses after fees on hourly trading. Daily gross ranges from -0.00036 to 0.00155 against daily fees of 0.00158 to 0.00341, and XMR has both the highest turnover (0.114 an hour) and a negative gross.

## Ideas
- `001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-trend-continuation.d1_week-averaged-rsi-strength-continuation` (from F1, F2, F3, F4, F6): The higher a coin's 14-day RSI has stood above 50 on average over the past 7 days, the more its price rises above its usual move over the next 10 days, most strongly while its 60-day return is positive.
- `001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-trend-continuation.d2_slow-rsi-strength-in-uptrends` (from F3, F5, F7): The higher a coin's 14-day RSI has stood above 50 on average over the past 7 days, the more its price rises above its usual move over the next 10 days, only while its 60-day return is positive.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
