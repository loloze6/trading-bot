---
brief: 021_ichimoku-cloud-as-a-watched-equilibrium
source-idea: 021-02_below-falling-cloud-continues-down.b1_slow-cloud-fall-continues.b1_slow-cloud-fall-more-coins
line: 7.g patterns
backtest: 021-02_below-falling-cloud-continues-down.b1_slow-cloud-fall-continues.b1_slow-cloud-fall-more-coins_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin closes below a falling Ichimoku cloud, its return over the next 26 days is more negative the more it has already fallen over the past 26 days.
Consequence: A coin that sits below a falling cloud after a steep 26-day drop is a reason to short it, while one below a falling cloud after a flat or rising month is a reason to refuse the short.
Why:
- F1: Below a falling cloud the coins rose on average: on the trending grid bars the 26-day forward return was +3.9 % (t 2.49, 353 cases), and the excess over each coin's drift was -1.8 % (t -1.17). The book's short earned its edge against the drift but lost on the total move, which fits the size block's total of -1.86 % per case and the 0.17 Sharpe against holding's 0.59.
- F2: Inside the trending regime, the past 26-day return sorts what follows far more than the cloud's slope does. The two lowest quartiles of the past 26-day return had excess 26-day returns of -15.4 % (t -6.4, 24 cases) and -16.5 % (t -3.2, 23 cases); the two highest had +3.4 % and +9.2 % (rank slope 0.37, time-clustered t 1.65 over 13 month-cells). The tested slow-fall gradient split at -0.12 Welch t.
- F5: The longest-held shorts were the only ones that paid. Trades in the top duration quartile, over about 37 days, earned +7.3 % net (348 trades); the shortest two quartiles lost -5.4 % and -9.6 % (372 and 472 trades), out of 1398 shorts with a mean of -3.2 %.
