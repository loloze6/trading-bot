---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-02_combination-beats-best-single.d1_combination-only-in-downtrends.d3_rebound-after-deep-declines
line: 7.d not profitable
backtest: 022-02_combination-beats-best-single.d1_combination-only-in-downtrends.d3_rebound-after-deep-declines_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's 90-day return is negative, the further it stands below its 90-day high, the higher its return over the next 10 days, the rise growing faster than the depth itself, so that most of the rebound comes from the deepest declines.
Consequence: A trader leans long only in proportion to how extreme the drawdown is, staying near flat at moderate drawdowns that keep drifting lower, and holds the rebound for longer than a week.
Why:
- F1: Inside the tested situation (90-day return below 0), the rebound exists only in the deepest declines. Below 60 % under the 90-day high, the 5-day excess return is +5.0 % (t 2.59, 67 cases, strength 0.44). From 46 to 60 % below it is +0.8 % (t 1.00, 208 cases). At every shallower depth, from 46 % below up to the high, it is negative, about -0.6 % to -1.0 % (for example t -2.02 on 425 cases from 20 to 35 % below). The relation is not linear, which is why the pooled linear slope has a t of only 0.79.
- F2: The book holds about the same position at every depth, so it carries the losing middle depths at full size. Its mean allocation is 0.46 below 60 %, 0.51 from 46 to 60 %, and 0.58 to 0.63 from 46 % below up to the high, because vol-target sizing undoes the depth gradient. Summed per-bar gains are +2.29 and +1.42 in the two deepest bins and -0.37, -0.07 and -0.09 from 35 % below up to the high.
- F4: The deep rebound outlasts the 5-day horizon. Below 60 % under the high, the 10-day forward return is +10.8 %, against +5.6 % over 5 days. From 46 to 60 % below it is +2.3 %, against +1.4 %.
- F5: The deep-decline rebound is spread over coins but not over every year. Below 46 % under the high, every coin's mean 5-day excess is positive (+0.7 % to +4.4 %), and 73 % of coin-windows are positive. Yet 2018 holds 130 of its 275 cases with a mean of -0.15 %, while 2020 to 2022 carry it (+9.5 %, +3.4 %, +2.2 %).
- F6: The tested idea's size at the tested depths is below the cost. Its unusual move is -0.44 % per case (strength -0.050), and its total move of +0.13 % is 0.7 times the 0.19 % round trip. Only the deepest cases (F1) have a move many times the cost.
