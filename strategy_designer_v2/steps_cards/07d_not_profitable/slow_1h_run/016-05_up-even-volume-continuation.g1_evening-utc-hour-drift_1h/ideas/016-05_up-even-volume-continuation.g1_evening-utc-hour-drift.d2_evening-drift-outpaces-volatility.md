---
brief: 016_grind-versus-jump-moves
source-idea: 016-05_up-even-volume-continuation.g1_evening-utc-hour-drift
line: 7.d not profitable
backtest: 016-05_up-even-volume-continuation.g1_evening-utc-hour-drift_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: Over the two hours after 20:00 UTC, the coin's rise measured in units of its 7-day hourly volatility is larger the higher that volatility is. So the rise grows faster than the coin's volatility, not just in proportion to it.
Consequence: The evening position should be held at the same or a larger size in volatile weeks rather than shrunk by volatility targeting, because that is where the gain per unit of risk is largest.
Why:
- F3: Almost all of the 2-hour rise sits in the coin's most volatile weeks. In the top decile of 7-day hourly volatility the return is +0.290% (t 4.0, n 1528) and in the ninth it is +0.124% (t 2.5). Deciles 0–7 range from -0.028% to +0.047%, with no t above 1.5. In volatility units it is still the top two deciles that carry it: 0.12 (t 3.6) and 0.09 (t 2.5), against at most 0.05 below.
- F5: The vol-target sizing puts the smallest position exactly where the gain is. The mean allocation is 0.34 in the top volatility decile and 0.64 in the bottom one. Most of the turnover, and so most of the fees, falls in the calm weeks that earn nothing.
