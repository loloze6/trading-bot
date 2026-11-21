---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-02_combination-beats-best-single
line: 7.g patterns
backtest: 022-02_combination-beats-best-single_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: On a Saturday, a coin's return over the next day is larger the higher its return over the preceding 7 days.
Consequence: A trader would lean long into the weekend on coins that rose over the past week, in proportion to that rise, and stay out of those that fell.
Why:
- F5: Saturday's daily return is the highest of the week. It averages +0.31 % above the coin's mean (t 3.78, 2365 days) and is above the rest of the week on all 6 coins (+0.04 % to +0.51 %, t vs rest 0.34 to 2.67) and in 6 of 8 years. Thursday (-0.32 %, t -2.87) and Tuesday (-0.23 %, t -2.43) are the lowest.
- F6: The Saturday rise grows with the coin's return over the preceding 7 days. By quintile of that return, Saturday's demeaned return is -0.13 %, -0.29 %, +0.13 %, +0.48 % (t 2.94) and +1.29 % (t 4.42, 360 days). In volatility units that is a mean z of +0.05, -0.08, +0.03, +0.15 and +0.28. The top quintile's move is about 6.8 times the 0.19 % round-trip cost.
- F7: Grouping Saturdays by the prior day's volatility, return or volume gives no ordered pattern. By prior 30-day volatility the quintile means are +0.35, +0.48, -0.12, +0.57 and +0.21 %. Only the prior week's return grades the Saturday move.
