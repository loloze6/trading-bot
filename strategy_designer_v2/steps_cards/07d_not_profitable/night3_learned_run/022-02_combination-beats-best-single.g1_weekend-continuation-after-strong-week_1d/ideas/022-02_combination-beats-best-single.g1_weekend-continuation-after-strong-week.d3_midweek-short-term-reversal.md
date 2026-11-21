---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-02_combination-beats-best-single.g1_weekend-continuation-after-strong-week
line: 7.d not profitable
backtest: 022-02_combination-beats-best-single.g1_weekend-continuation-after-strong-week_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: On a Wednesday, a coin's return over the next day is larger the lower its return over the preceding 3 days.
Consequence: A trader would lean long into Wednesday on coins that fell over the past 3 days, in proportion to the fall, and away from coins that rose.
Why:
- F4: Wednesday also shows a reversal of the 3-day return: correlation -0.113 with the next day's excess return, over 1859 cases.
- F1: The book fails on mean daily return (0.000288 against 0.0005) because it is invested only one day a week, not because trades cost too much. It holds a position on 6.1 % of bars, at a mean allocation of 0.58, and earns 0.25 % per active bar. Each case's total move (+0.90 %) is 4.7 times the 0.19 % cost of a trade.
