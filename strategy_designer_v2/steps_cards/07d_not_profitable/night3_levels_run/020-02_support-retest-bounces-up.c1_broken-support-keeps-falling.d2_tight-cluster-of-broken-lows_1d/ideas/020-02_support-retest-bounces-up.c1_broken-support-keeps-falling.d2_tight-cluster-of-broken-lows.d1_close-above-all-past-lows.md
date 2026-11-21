---
brief: 020_support-and-resistance-at-past-turning-prices
source-idea: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.d2_tight-cluster-of-broken-lows
line: 7.d not profitable
backtest: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.d2_tight-cluster-of-broken-lows_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's daily close sits above every price where it turned up in the past 90 days, it tends to rise over the next 5 days. The farther the close sits above the highest of those past turning-up lows, the larger the rise.
Consequence: A trader should hold a long while the close sits above all its recent turning-up lows, and stand aside rather than short when such lows sit above it.
Why:
- F1: The book lost because it was short against rising coins. Its mean position was -0.48 and it was short 75 % of bars. Holding short against the coins' own rise cost -0.057 % per bar, while its timing earned +0.030 %, for a net of -0.028 % per bar. That net was negative in 5 of 8 years and on all 6 coins.
- F3: The forecast does rank what follows, but on the long side. Bars with no past-90-day swing low above the close rose most, +1.37 % over 5 days (+0.79 % above the coin's drift, 1060 cases). From there the rise shrinks steadily as the short grows: +0.81 %, +0.10 %, -0.20 %.
- F2: Even where the short signal was strongest, the coin barely fell, so a short on this idea cannot cover the 0.19 % cost of a trade.
