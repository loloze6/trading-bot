---
brief: 021_ichimoku-cloud-as-a-watched-equilibrium
source-idea: 021-02_below-falling-cloud-continues-down.d2_below-thin-falling-cloud
line: 7.d not profitable
backtest: 021-02_below-falling-cloud-continues-down.d2_below-thin-falling-cloud_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin closes below its Ichimoku cloud and the cloud is falling, its return over the next 26 days is negative, and more negative the thinner the cloud is relative to the price, only while the coin's close is near its 26-day high rather than far below it.
Consequence: A trader would keep shorts below a thin falling cloud when the coin has not yet fallen far from its recent high, and refuse them after a deep fall, where the coin's upward drift and rebound overwhelm the continuation.
Why:
- F1: The book loses before any cost because the total move per case runs against the short: the coin's normal drift is +4.15 % over 26 days, the unusual move only +2.79 %, so the total is -1.36 % per case (241 cases), against a cost of 0.19 %. On the bars where the book is short the coin still rose +0.069 % a day (+0.119 % on all bars), and the short bars earned -0.040 % a day, giving a book Sharpe of -0.31 and a mean daily return of -0.0002.
- F2: Thinness grades the move as the idea says, and the losses sit in the thick-cloud cases. In the thickest third of the forecast (mean |forecast| 2.4, 52 cases) the total move is -8.7 % (unusual -4.3 %). In the middle third it is -0.5 % (unusual +3.8 %). In the thinnest third (|forecast| 14.6) it is +1.0 % (unusual +5.0 %), with a Spearman between |forecast| and the excess return of p 0.008 over 156 cases.
- F4: The fall from the 26-day high also grades the result: in the third deepest below that high (mean -36 %) the short's total is -5.7 % per case, in the shallowest third (mean -10 %) it is +1.9 %.
- F5: The book's deepest falls come from staying short through the coins' rallies: in w21 the book lost 23 % (deepest fall 25 %) while the coins rose 87 %. In w8, w16, w17 and w6 it lost 13 to 21 % while the coins rose 29 to 48 %.
