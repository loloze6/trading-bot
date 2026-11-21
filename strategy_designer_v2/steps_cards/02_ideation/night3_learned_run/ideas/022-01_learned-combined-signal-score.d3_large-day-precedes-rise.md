---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-01_learned-combined-signal-score
line: 7.d not profitable
backtest: 022-01_learned-combined-signal-score_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's absolute return over its last day, the higher its return over the next 5 days.
Consequence: Treat a day of unusually large movement, up or down, as a reason to lean long the coin for the following 5 days.
Why:
- F8: Days with the largest absolute move are followed by higher returns. The top fifth of the absolute 1-day return is followed by +0.93 % excess (strength 0.078, t 1.93, 628 cases) and +1.60 % total over 5 days. The second and third fifths are followed by -0.86 % and -0.99 % (t -2.2 and -2.4).
- F3: Both sides lose. Long cases earn -0.56 % excess per 5 days (t -2.10, 1535 cases) and short cases -0.49 % (t -1.83, 1743 cases). The two most negative forecast quintiles are followed by +0.67 % and +0.63 % excess moves, and the fourth quintile by -1.19 %.
