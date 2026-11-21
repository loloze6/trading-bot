---
brief: 021_ichimoku-cloud-as-a-watched-equilibrium
source-idea: 021-02_below-falling-cloud-continues-down.d2_below-thin-falling-cloud
line: 7.d not profitable
backtest: 021-02_below-falling-cloud-continues-down.d2_below-thin-falling-cloud_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin closes below a thick falling Ichimoku cloud after falling over the past 7 days, its return over the next 26 days is positive, and larger the thicker the cloud is relative to the price and the deeper its 7-day fall.
Consequence: A trader would take longs, not shorts, in the rebound below a thick falling cloud after a sharp week's fall, with the coin's normal upward drift on the trade's side.
Why:
- F1: The book loses before any cost because the total move per case runs against the short: the coin's normal drift is +4.15 % over 26 days, the unusual move only +2.79 %, so the total is -1.36 % per case (241 cases), against a cost of 0.19 %. On the bars where the book is short the coin still rose +0.069 % a day (+0.119 % on all bars), and the short bars earned -0.040 % a day, giving a book Sharpe of -0.31 and a mean daily return of -0.0002.
- F2: Thinness grades the move as the idea says, and the losses sit in the thick-cloud cases. In the thickest third of the forecast (mean |forecast| 2.4, 52 cases) the total move is -8.7 % (unusual -4.3 %). In the middle third it is -0.5 % (unusual +3.8 %). In the thinnest third (|forecast| 14.6) it is +1.0 % (unusual +5.0 %), with a Spearman between |forecast| and the excess return of p 0.008 over 156 cases.
- F3: The worst cases are a thick cloud after a 7-day fall: the coin then rose about 20 % over 26 days (total -19.9 %, unusual -15.9 %, 28 cases). Under a thick cloud after a 7-day rise the short earned +6.1 % total (31 cases). Under a thin cloud the short earned +5.7 % after a 7-day fall (31 cases) and +0.8 % after a 7-day rise (28 cases).
