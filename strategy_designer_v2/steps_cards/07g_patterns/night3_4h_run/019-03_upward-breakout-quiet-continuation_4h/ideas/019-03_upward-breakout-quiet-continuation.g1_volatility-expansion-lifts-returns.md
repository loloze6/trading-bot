---
brief: 019_quiet-range-then-breakout-on-four-hour-bars
source-idea: 019-03_upward-breakout-quiet-continuation
line: 7.g patterns
backtest: 019-03_upward-breakout-quiet-continuation_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: The more a coin's 3-day realised volatility exceeds its 30-day realised volatility, the more the coin rises over the next 3 days.
Consequence: A trader leans long a coin whose last three days were far more volatile than its month, and refuses longs in its quietest stretches.
Why:
- F1: Over the next 3 days, a coin rises more when its last 3 days were unusually volatile against its 30-day volatility (its 18-bar standard deviation of 4h returns over its 180-bar one). The top decile of that ratio was followed by an excess return of +0.242 of the usual 3-day move, which is +2.05 % (t 4.75, 515 non-overlapping cases), about 10 times the 0.19 % cost of a buy and a sell. The other nine deciles lie between -0.108 and +0.041.
- F2: The volatility-expansion effect of F1 holds on every coin and in every year but one. The top quintile minus the bottom quintile is positive on all 6 coins (+0.06 on ETH to +0.36 on LTC, in usual moves) and in 7 of 8 years (2025 is flat at +0.027 against +0.026).
- F3: The same pattern shows on the bar range. When the last 3 days' mean 4h range is high against its 30-day mean, the excess 3-day return is +0.137 (t 2.87) and +0.128 (t 2.30) in its two top deciles. The bottom decile gives -0.089 (t -1.99), 515 cases each.
- F4: A wide recent range helps after both a 3-day rise and a 3-day fall, but more after a rise. After a rise, the top third by recent range gives +0.094 (t 2.45, 901 cases) against -0.013 for the bottom third. After a fall, the top third gives +0.045 (t 1.20) against -0.062 (t -2.02).
