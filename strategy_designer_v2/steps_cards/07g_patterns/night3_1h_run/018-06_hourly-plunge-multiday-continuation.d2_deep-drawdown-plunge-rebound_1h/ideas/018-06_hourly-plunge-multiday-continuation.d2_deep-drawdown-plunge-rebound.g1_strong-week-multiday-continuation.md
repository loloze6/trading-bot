---
brief: 018_daily-condition-caught-on-the-hour
source-idea: 018-06_hourly-plunge-multiday-continuation.d2_deep-drawdown-plunge-rebound
line: 7.g patterns
backtest: 018-06_hourly-plunge-multiday-continuation.d2_deep-drawdown-plunge-rebound_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's 7-day rise in multiples of its 30-day average absolute 7-day return, the larger its rise over the next 3 days.
Consequence: A trader should favour buying coins after an unusually strong week and refuse to fade such weeks, since the continuation that follows is several times the cost of a trade.
Why:
- F1: Across 6 coins and 24 windows, the fifth of 72-hour grid cases with the largest 7-day rise, measured in multiples of the coin's 30-day mean absolute 7-day return (mean 2.06), was followed by an unusual move of +1.03 % over the next 3 days (strength 0.122, t 3.40, 909 cases); they beat the other four fifths by +1.23 % (Welch t 3.69, 909 vs 3622 cases).
- F3: The 3-day effect after a strong 7-day rise holds on all 6 coins: +0.47 % on LTC to +2.06 % on XRP, t 0.70 to 2.05, about 150 cases each. It is positive in 6 of 8 years, negative in 2022 (−1.37 %, t −1.67) and about zero in 2023. It is stronger in the later half of the windows (+1.57 %, t 3.36) than in the earlier half (+0.45 %, t 1.19).
- F4: The effect sits in the tail only. Over all cases, each coin's rank correlation between the scaled 7-day return and the next 3 days' unusual move is about zero (rho −0.022 to +0.028). The middle three fifths have unusual moves of −0.27 % to −0.34 %, and the bottom fifth +0.10 %.
- F5: Per case over 3 days, the strong-week unusual move of +1.03 % is about 5.4 times the 0.19 % cost of a buy and a sell in this backtest. The tested deep-drawdown plunge idea had an unusual move of −0.15 % (−0.8 times the cost), consistent with the size findings F10 and F11.
