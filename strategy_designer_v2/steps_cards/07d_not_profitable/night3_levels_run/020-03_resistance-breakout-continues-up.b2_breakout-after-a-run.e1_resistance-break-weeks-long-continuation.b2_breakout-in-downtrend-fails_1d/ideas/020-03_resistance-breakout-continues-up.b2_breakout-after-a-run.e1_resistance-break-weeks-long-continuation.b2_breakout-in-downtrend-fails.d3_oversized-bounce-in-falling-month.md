---
brief: 020_support-and-resistance-at-past-turning-prices
source-idea: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.e1_resistance-break-weeks-long-continuation.b2_breakout-in-downtrend-fails
line: 7.d not profitable
backtest: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.e1_resistance-break-weeks-long-continuation.b2_breakout-in-downtrend-fails_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin rises sharply in one day while its 30-day return is negative, it tends to fall back over the next 20 days. The larger that one-day rise against its 30-day daily volatility, the larger the decline.
Consequence: A large one-day bounce in a falling coin is a reason to refuse a long, whatever price level it crosses.
Why:
- F3: The depth of the 30-day fall grades the outcome as the idea says. In the deepest quartile (mean 30-day return -50 %) the short gain is +3.8 % (t 1.74, 60 entries). In the shallowest quartile (-2.8 %) it is -5.6 % (t -1.48). Spearman rho between the 30-day return and the short gain is -0.13.
- F4: The size of the break day's own rise grades the reversal. In the largest one-day-rise quartile (mean +10.8 %) the short gain is +4.7 % (t 1.62, 56 entries). In the smallest quartile (+1.3 %) it is -7.9 % (t -2.08). Spearman rho is +0.15.
- F5: The level's strength (touch count times margin) carries no grading. Its quartiles give short gains of +1.1 %, -2.9 %, -5.2 % and +1.8 %, and Spearman rho is 0.04.
- F6: Shorts entered in calm coins lose. In the lowest 30-day volatility quartile (daily standard deviation 1.5 %) the short gain is -7.1 % (t -2.13, 56 entries). In the third quartile (4.4 %) it is +4.9 % (t 1.76). Spearman rho is +0.16.
