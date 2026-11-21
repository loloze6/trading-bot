---
brief: 020_support-and-resistance-at-past-turning-prices
source-idea: 020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.b2_false-breakout-in-downtrend
line: 7.d not profitable
backtest: 020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.b2_false-breakout-in-downtrend_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's 30-day return turns from negative to positive, the coin rises over the next 10 days, and the larger its new 30-day return, the larger the rise.
Consequence: A trader should refuse to be short a coin whose 30-day return has just turned positive, and may lean long in proportion to the size of the turn.
Why:
- F1: The whole loss of the book comes from shorts still held after the coin's 30-day return had turned positive. Shorts held while the regime was still "mean_reversion" (30-day return below 0) earned +4.43 in summed bar gains over 10,304 bars. Shorts carried into the "unknown" regime lost -6.55 over 3,374 bars. The book's total is -2.11 before about 1.76 of fees.
- F2: Being short in the wrong place is what loses, not the signal itself. On the bars the book was short, the coin's mean next-day return was -0.023 %. On flat bars it was +0.242 %. Bars in the unknown regime lost about 0.19 % each at a mean short size of 0.79. In those bars the coins were rising about 0.25 % a day, roughly 2.5 % over 10 days, which is larger than the idea's whole unusual move of +1.79 %.
