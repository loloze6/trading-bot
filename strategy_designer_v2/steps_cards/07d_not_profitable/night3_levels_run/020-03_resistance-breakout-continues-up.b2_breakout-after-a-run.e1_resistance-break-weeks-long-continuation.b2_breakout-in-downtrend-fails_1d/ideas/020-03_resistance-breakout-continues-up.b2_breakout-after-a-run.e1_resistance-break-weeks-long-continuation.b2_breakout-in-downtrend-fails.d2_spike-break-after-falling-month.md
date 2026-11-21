---
brief: 020_support-and-resistance-at-past-turning-prices
source-idea: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.e1_resistance-break-weeks-long-continuation.b2_breakout-in-downtrend-fails
line: 7.d not profitable
backtest: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.e1_resistance-break-weeks-long-continuation.b2_breakout-in-downtrend-fails_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin closes above a price where it turned down several times in the past 90 days after its 30-day return was negative, it tends to fall back over the next 20 days. The larger that day's own rise against the coin's 30-day daily volatility, and the deeper the 30-day fall, the larger the decline.
Consequence: A sharp one-day spike through resistance during a falling month is a reason to sell; a small drift-through is not.
Why:
- F1: The book loses because it shorts coins that rise in most windows. Measured on the step 5 cases, the idea's unusual move is +1.99 % per case over 20 days, but the coin's normal drift in the short direction is -2.51 %. So the total move is -0.52 % per case, which is -2.7 times the 0.19 % cost of a round trip. On the book's own 239 short entries, the mean 20-day short gain is -1.32 % (t -0.86, 54 % winners).
- F3: The depth of the 30-day fall grades the outcome as the idea says. In the deepest quartile (mean 30-day return -50 %) the short gain is +3.8 % (t 1.74, 60 entries). In the shallowest quartile (-2.8 %) it is -5.6 % (t -1.48). Spearman rho between the 30-day return and the short gain is -0.13.
- F4: The size of the break day's own rise grades the reversal. In the largest one-day-rise quartile (mean +10.8 %) the short gain is +4.7 % (t 1.62, 56 entries). In the smallest quartile (+1.3 %) it is -7.9 % (t -2.08). Spearman rho is +0.15.
- F6: Shorts entered in calm coins lose. In the lowest 30-day volatility quartile (daily standard deviation 1.5 %) the short gain is -7.1 % (t -2.13, 56 entries). In the third quartile (4.4 %) it is +4.9 % (t 1.76). Spearman rho is +0.16.
