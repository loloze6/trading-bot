---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-02_combination-beats-best-single.g1_weekend-continuation-after-strong-week
line: 7.d not profitable
backtest: 022-02_combination-beats-best-single.g1_weekend-continuation-after-strong-week_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: On a Saturday, a coin's return over the next day is larger the higher its return over the preceding 7 days, and on a Sunday, a coin's return over the next day is larger the lower its return over the preceding 7 days.
Consequence: A trader would lean long into Saturday on coins that rose over the past week and then lean long into Sunday on coins that fell over it, in proportion to the size of the week's move, which puts the book to work two days a week instead of one.
Why:
- F1: The book fails on mean daily return (0.000288 against 0.0005) because it is invested only one day a week, not because trades cost too much. It holds a position on 6.1 % of bars, at a mean allocation of 0.58, and earns 0.25 % per active bar. Each case's total move (+0.90 %) is 4.7 times the 0.19 % cost of a trade.
- F2: The 7-day continuation exists on Saturday only. The correlation of the 7-day return with the next day's excess return is 0.185 on Saturdays (rising minus falling weeks, Welch t 4.68, 1172 rising cases). On every other day the correlation lies between -0.07 and +0.07, so stretching this same signal to more days adds no gain.
- F3: Sunday shows the opposite effect, a reversal. The next-day excess return correlates -0.093 with the 7-day return and -0.102 with the 1-day return. Rising weeks minus falling weeks give Welch t -2.49. The quintile with the lowest combined momentum earns +0.69 % on Sunday (t 2.98, 378 cases), and the other quintiles are flat to negative.
- F5: The Saturday effect is graded. Next-day excess returns by 7-day-return quintile run -0.19 %, -0.04 %, +0.22 %, +0.60 %, +0.99 %. It does not grow when held longer: the top quintile is +0.88 % after 2 days and +0.42 % after 3, so it gives back part of the gain on Sunday.
