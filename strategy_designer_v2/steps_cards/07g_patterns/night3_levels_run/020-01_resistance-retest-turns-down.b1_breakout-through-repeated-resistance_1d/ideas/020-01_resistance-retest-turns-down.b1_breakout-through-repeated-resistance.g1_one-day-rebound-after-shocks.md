---
brief: 020_support-and-resistance-at-past-turning-prices
source-idea: 020-01_resistance-retest-turns-down.b1_breakout-through-repeated-resistance
line: 7.g patterns
backtest: 020-01_resistance-retest-turns-down.b1_breakout-through-repeated-resistance_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin closes a day with a fall that is large compared with its own daily moves of the past 20 days, it tends to rise over the next day, and the larger the fall relative to that 20-day volatility, the larger the next day's rise.
Consequence: A sharp down day relative to the coin's recent volatility is a reason to buy for a one-day rebound, more so the larger the fall, and a reason not to sell into it.
Why:
- F1: Unusually large one-day falls are followed by a next-day rebound. Measured against each coin's last 20 days of volatility, days in the lowest twentieth were followed by a next-day excess return of +0.43 % (t 1.97, 719 cases), and days in the next twentieth by +0.63 % (t 3.16, 718 cases). Ranking raw one-day returns gives the same picture: the worst tenth of days was followed by +0.88 % the next day (t 5.81, 1728 cases), and the next two tenths by +0.26 % and +0.22 % (t 2.11 and 1.95).
- F2: The rebound is graded and broad. On down days, the rank correlation between the size of the fall and the next day's excess return is negative in all 6 coins (-0.03 BTC to -0.10 XMR). After the worst tenth of days, the next-day excess is positive in 6 of 6 coins (+0.26 % BTC to +0.91 % XMR; XMR t 2.94), in 7 of 8 years (largest in 2020, +1.50 % with t 2.76, and 2021, +1.20 % with t 2.43), and in 75 % of windows.
- F3: The rebound is a one-day move. Over the next 3 days, the two worst twentieths show +0.46 % and +0.93 % (t 0.95 and 1.38, about 230 cases each), not distinguishable from chance. Its size per case, about 0.4 to 0.9 %, is 2 to 4 times this backtest's round-trip cost of 0.19 %.
- F4: The book's gain rides partly on this rebound, which the idea does not explain. On the worst tenth of days, the next-day excess return was +0.81 % when the book held a position (988 cases) and -0.09 % when it was flat (449 cases).
