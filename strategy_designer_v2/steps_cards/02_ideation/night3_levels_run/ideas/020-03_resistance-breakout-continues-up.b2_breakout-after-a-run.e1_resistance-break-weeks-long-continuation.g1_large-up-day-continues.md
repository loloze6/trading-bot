---
brief: 020_support-and-resistance-at-past-turning-prices
source-idea: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.e1_resistance-break-weeks-long-continuation
line: 7.g patterns
backtest: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.e1_resistance-break-weeks-long-continuation_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin closes a day with a rise that is large against its own 20-day volatility, it tends to keep rising over the next 5 days. The larger that day's rise relative to its 20-day volatility, the larger the rise that follows.
Consequence: A day of unusually strong gain, measured against the coin's recent volatility, is a reason to be long for the following week rather than to fade it.
Why:
- F3: A day whose return is large against the coin's 20-day volatility is followed by a rise over the next 5 days, measured on a 5-day grid with each coin's drift removed:
- F4: This top-quintile rise holds in both halves of the windows: +1.28 % (t 2.14, 276 cases) in w1-12 and +1.88 % (t 2.36, 294 cases) in w13-24. It is positive on 5 of 6 coins (BTC +1.6 %, ZEC +3.7 %, XRP +2.6 %; LTC -0.03 %).
- F5: Among positive days, the size of the day's move ranks with the next 5 days' excess return on all 6 coins (Spearman 0.03 to 0.09). The move per case, about 1.6 %, is roughly 8 times the backtest's 0.19 % round trip.
- F6: Over 3 days and 10 days the large-day effect is weak: the top decile gives +0.71 % (t 1.54) at 3 days and +2.21 % (t 1.28, 144 cases) at 10 days. The 5-day reading is the clearest, and it is one of about twenty angles examined.
