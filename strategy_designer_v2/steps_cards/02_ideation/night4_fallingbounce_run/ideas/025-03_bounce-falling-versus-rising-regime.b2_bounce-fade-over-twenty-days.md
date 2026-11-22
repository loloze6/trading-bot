---
brief: 025_bounces-fade-in-falling-markets
source-idea: 025-03_bounce-falling-versus-rising-regime
line: 7.b inconclusive
backtest: 025-03_bounce-falling-versus-rising-regime_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In one coin, the 20-day return after a one-day rise of several usual daily moves (its day's return over the standard deviation of its last 20 daily returns) is lower when its 90-day return is negative than when it is positive, and the gap widens as the rise gets larger.
Consequence: A trader would treat a sharp bounce in a coin down over 90 days as a weaker basis for a long over the following weeks than the same bounce in a coin up over 90 days, more so the sharper the bounce.
Why:
- F1: The tested gap (long cases minus short cases, 5-day excess return) is on the side the idea predicts but small at +0.35 % (Welch t 0.87; 1510 long and 1319 short cases); it grows with the horizon to +0.58 % at 10 days (t 0.92) and +1.65 % at 20 days (t 1.57, 1338 / 1150 cases), and turns negative at 1 day (−0.12 %, t −0.67) and 3 days (−0.30 %, t −0.96).
- F4: The test's grading barely separates the cases. 52 % of the cases sit at the forecast cap of 20 (median |forecast| 18.9), while their rise is only 1.6 usual daily moves at the median. The forecast-tercile gaps are flat rather than widening: +0.48 % (t 0.72), +0.45 % (t 0.70) and +0.14 % (t 0.19).
- F6: Measured instead by the rise in usual 20-day moves, the regime gap appears at the largest rises. Above 3 usual moves, the 5-day excess return is +3.38 % in rising coins (t 2.17, n 108) against −0.66 % in falling ones (n 68). Between 2 and 2.5 moves it is +1.08 % against −1.36 % (n 103 / 96). Below 1.5 moves the two regimes are equal (−1.65 % against −1.68 %).
- F7: The idea is small against the cost of a trade. Its unusual move is +0.17 % per case (strength 0.017) and its total move is +0.20 %, against a trade cost of 0.19 %. The book's Sharpe is 0.12, against holding's 0.55.
