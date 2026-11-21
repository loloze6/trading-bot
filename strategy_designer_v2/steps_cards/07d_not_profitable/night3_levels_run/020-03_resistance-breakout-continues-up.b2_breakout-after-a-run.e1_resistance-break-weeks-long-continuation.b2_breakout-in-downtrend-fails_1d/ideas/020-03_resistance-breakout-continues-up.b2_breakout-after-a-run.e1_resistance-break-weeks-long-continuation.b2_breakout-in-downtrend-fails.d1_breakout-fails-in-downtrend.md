---
brief: 020_support-and-resistance-at-past-turning-prices
source-idea: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.e1_resistance-break-weeks-long-continuation.b2_breakout-in-downtrend-fails
line: 7.d not profitable
backtest: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.e1_resistance-break-weeks-long-continuation.b2_breakout-in-downtrend-fails_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin closes above a price where it turned down several times in the past 90 days after its 30-day return was negative, it tends to fall back over the next 20 days, only while its 90-day return is also negative. The deeper that 30-day fall, the larger the decline.
Consequence: Shorting a break after a falling month pays only when the coin's own longer trend is also down; in a rising coin, the coin's rise outweighs the reversal.
Why:
- F1: The book loses because it shorts coins that rise in most windows. Measured on the step 5 cases, the idea's unusual move is +1.99 % per case over 20 days, but the coin's normal drift in the short direction is -2.51 %. So the total move is -0.52 % per case, which is -2.7 times the 0.19 % cost of a round trip. On the book's own 239 short entries, the mean 20-day short gain is -1.32 % (t -0.86, 54 % winners).
- F2: The short entries pay only in falling years. In 2018 they earned +9.4 % per entry (t 2.45, 27 entries, coin 20-day drift -9.6 %), and in 2022 +7.0 % (t 2.32, 33 entries, drift -3.5 %). They lose in the rising years, for example 2024 at -6.4 % (t -2.13, drift +5.2 %) and 2023 at -5.2 % (t -1.51). The book's mean daily return is above 0 only in 2018 (+0.00043), 2022 (+0.00063) and 2025 (+0.00049).
- F3: The depth of the 30-day fall grades the outcome as the idea says. In the deepest quartile (mean 30-day return -50 %) the short gain is +3.8 % (t 1.74, 60 entries). In the shallowest quartile (-2.8 %) it is -5.6 % (t -1.48). Spearman rho between the 30-day return and the short gain is -0.13.
