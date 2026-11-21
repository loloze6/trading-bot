---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-02_combination-beats-best-single.g1_weekend-continuation-after-strong-week
line: 7.d not profitable
backtest: 022-02_combination-beats-best-single.g1_weekend-continuation-after-strong-week_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: On a Sunday, a coin's return over the next day is larger the lower its return over the preceding 7 days.
Consequence: A trader would buy on Saturday's close the coins that fell most over the past week, in proportion to the fall, and refuse that trade on coins that rose.
Why:
- F3: Sunday shows the opposite effect, a reversal. The next-day excess return correlates -0.093 with the 7-day return and -0.102 with the 1-day return. Rising weeks minus falling weeks give Welch t -2.49. The quintile with the lowest combined momentum earns +0.69 % on Sunday (t 2.98, 378 cases), and the other quintiles are flat to negative.
- F5: The Saturday effect is graded. Next-day excess returns by 7-day-return quintile run -0.19 %, -0.04 %, +0.22 %, +0.60 %, +0.99 %. It does not grow when held longer: the top quintile is +0.88 % after 2 days and +0.42 % after 3, so it gives back part of the gain on Sunday.
