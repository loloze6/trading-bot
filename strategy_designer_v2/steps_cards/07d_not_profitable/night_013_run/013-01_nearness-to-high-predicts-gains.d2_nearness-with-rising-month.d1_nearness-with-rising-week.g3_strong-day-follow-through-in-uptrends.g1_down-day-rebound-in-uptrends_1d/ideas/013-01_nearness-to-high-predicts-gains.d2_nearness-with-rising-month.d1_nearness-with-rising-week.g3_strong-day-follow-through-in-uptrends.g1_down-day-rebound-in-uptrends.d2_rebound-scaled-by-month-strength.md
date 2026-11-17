---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g3_strong-day-follow-through-in-uptrends.g1_down-day-rebound-in-uptrends
line: 7.d not profitable
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g3_strong-day-follow-through-in-uptrends.g1_down-day-rebound-in-uptrends_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's 30-day return is positive, the larger its latest one-day fall relative to its 30-day daily volatility, the higher its return over the next 1 day, and the larger that coin's 30-day return, the larger this rebound.
Consequence: A trader should buy sharp down days mainly in coins with a strong 30-day rise, and pass on those whose month is barely positive.
Why:
- F4: The rebound grows with the strength of the 30-day rise, with next-1-day return -0.0016 (t -1.12), 0.0010, 0.0040 (t 2.33), 0.0053 (t 2.89) and 0.0050 across 30-day-return quintiles (n≈592 each); the non-overlapping 3-day return runs -0.0015, 0.0022, 0.0077 and 0.0203 across quartiles (n≈240 each).
- F5: The mean daily return is held down by small, fee-heavy exposure: the book is long on only 23% of bars, with a mean allocation of 0.094; fees take 42% of the gross gain (0.000160 of 0.000381 per bar); in the two weakest forecast quintiles, fees (0.000143, 0.000233) match or exceed the gain (0.000115, 0.000234).
- F6: The gain is concentrated in the largest falls, with a next-1-day return of 0.0070 and gain 0.0057 per bar in the top forecast quintile, against 0.0014 and 0.0001 in the bottom one.
