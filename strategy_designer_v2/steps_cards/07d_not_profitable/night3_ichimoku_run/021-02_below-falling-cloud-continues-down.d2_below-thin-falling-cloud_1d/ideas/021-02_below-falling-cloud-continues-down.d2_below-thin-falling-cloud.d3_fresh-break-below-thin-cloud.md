---
brief: 021_ichimoku-cloud-as-a-watched-equilibrium
source-idea: 021-02_below-falling-cloud-continues-down.d2_below-thin-falling-cloud
line: 7.d not profitable
backtest: 021-02_below-falling-cloud-continues-down.d2_below-thin-falling-cloud_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin closes below its Ichimoku cloud and the cloud is falling, its return over the next 26 days is negative, and more negative the thinner the cloud is relative to the price, only while the coin first closed below the cloud within the past few weeks rather than over a month ago.
Consequence: A trader would short fresh breaks below a thin falling cloud and refuse shorts on coins that have stayed below the cloud for over a month, where the downtrend is exhausted.
Why:
- F1: The book loses before any cost because the total move per case runs against the short: the coin's normal drift is +4.15 % over 26 days, the unusual move only +2.79 %, so the total is -1.36 % per case (241 cases), against a cost of 0.19 %. On the bars where the book is short the coin still rose +0.069 % a day (+0.119 % on all bars), and the short bars earned -0.040 % a day, giving a book Sharpe of -0.31 and a mean daily return of -0.0002.
- F2: Thinness grades the move as the idea says, and the losses sit in the thick-cloud cases. In the thickest third of the forecast (mean |forecast| 2.4, 52 cases) the total move is -8.7 % (unusual -4.3 %). In the middle third it is -0.5 % (unusual +3.8 %). In the thinnest third (|forecast| 14.6) it is +1.0 % (unusual +5.0 %), with a Spearman between |forecast| and the excess return of p 0.008 over 156 cases.
- F5: The book's deepest falls come from staying short through the coins' rallies: in w21 the book lost 23 % (deepest fall 25 %) while the coins rose 87 %. In w8, w16, w17 and w6 it lost 13 to 21 % while the coins rose 29 to 48 %.
- F6: Long-lasting regimes lose. In the third of cases where the coin had been below the falling cloud for the longest (mean 34 days) the short's total is -7.3 %, against +2.0 % in the middle third (mean 10 days).
