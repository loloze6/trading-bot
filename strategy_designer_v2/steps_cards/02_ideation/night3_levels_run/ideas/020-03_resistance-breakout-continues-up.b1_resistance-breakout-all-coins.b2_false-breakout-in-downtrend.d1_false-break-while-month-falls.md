---
brief: 020_support-and-resistance-at-past-turning-prices
source-idea: 020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.b2_false-breakout-in-downtrend
line: 7.d not profitable
backtest: 020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.b2_false-breakout-in-downtrend_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin closes above a price where it turned down several times in the past 90 days while its 30-day return is negative, it tends to fall back over the next 10 days, and the deeper its 30-day decline, the larger the fall, only while its 30-day return is still negative on each of those days; the fall is largest when the 30-day return stays deeply negative through the 10 days.
Consequence: A trader fading a break of a repeatedly-held high in a falling month should hold the fade only as long as the month is still down, and drop it as soon as the coin's 30-day return turns positive.
Why:
- F1: The whole loss of the book comes from shorts still held after the coin's 30-day return had turned positive. Shorts held while the regime was still "mean_reversion" (30-day return below 0) earned +4.43 in summed bar gains over 10,304 bars. Shorts carried into the "unknown" regime lost -6.55 over 3,374 bars. The book's total is -2.11 before about 1.76 of fees.
- F2: Being short in the wrong place is what loses, not the signal itself. On the bars the book was short, the coin's mean next-day return was -0.023 %. On flat bars it was +0.242 %. Bars in the unknown regime lost about 0.19 % each at a mean short size of 0.79. In those bars the coins were rising about 0.25 % a day, roughly 2.5 % over 10 days, which is larger than the idea's whole unusual move of +1.79 %.
- F3: The idea is real but thin once the drift is counted. Per case, the unusual move is +1.79 % (strength 0.098), while the coin's normal drift against the short is -1.38 %. The total move is only +0.41 %, 1.8 times the 0.22 % round trip. Any loss from holding past the move wipes it out.
- F4: Holding runs past the idea's 10-day horizon, and those extra days lose. The 2,229 short trades lasted 11.3 days on average, with a mean gross of -3.38 %, a net of -3.49 % and 35 % winners. The 595 trades lasting 10 to 20 days lost a mean of -4.35 % to -6.18 % net. The case-level total move over exactly 10 days is +0.41 %.
