---
brief: 010_rsi-midline-regime-direction
source-idea: 010-03_rsi-above-streak-continuation.e2_below-midline-streak-continues-down
line: 7.g patterns
backtest: 010-03_rsi-above-streak-continuation.e2_below-midline-streak-continues-down_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: Once a coin's 14-day RSI has stayed below 50 for weeks, the longer that unbroken stretch has lasted up to the close, the higher the coin's return over the next 7 days.
Consequence: A very long stretch of seller control is a reason to cover shorts or buy the coin for the following week, not to press the short.
Why:
- F1: Among grid bars where the 14-day RSI had been below 50 for 14 days or more (134 cases), the excess 7-day return rose with the length of the stretch (OLS slope +0.0031 per day, t 3.42), and the slope holds in each coin on its own (BTC t 2.15 on 61 cases, ETH t 2.62 on 73), the opposite direction to the tested idea.
- F2: By bucket of the signed RSI-side run, stretches below 50 of 30 days or more were followed by +3.4% excess over 7 days (n 43, t 2.01), while stretches of 14 to 30 days were followed by -3.0% (n 91, t -2.61), so the sign flips as the stretch lengthens; the long-stretch cases come from only 12 windows and are strongest in 2018 (+8.4%, n 12) and 2020 (+5.1%, n 6).
- F3: Over all below-50 grid bars the run length shows no monotone link to the excess 7-day return (Spearman rho 0.05, p 0.35; plan slope t 1.15), so the tested continuation reading is absent and the book earned nothing (daily mean 1.4e-05, Sharpe 0.019; its 29 worst days sum to -2.17 and its 29 best to +2.14).
