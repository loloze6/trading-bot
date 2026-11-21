---
brief: 020_support-and-resistance-at-past-turning-prices
source-idea: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b2_broken-support-ten-day-fall.c2_broken-support-in-downtrend
line: 7.d not profitable
backtest: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b2_broken-support-ten-day-fall.c2_broken-support-in-downtrend_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's daily close sits just below prices where it turned up several times in the past 90 days, it tends to fall over the next 10 days, and the more such past turning-up lows lie just above the close, the larger the fall, only while its 60-day return is negative. The fall is larger the more lows cluster there and the nearer the close sits under them, by enough that the strongest clusters outweigh the coin's usual 10-day rise.
Consequence: Only the largest, nearest clusters justify a short against the coin's upward drift; weak readings are a reason to stay flat.
Why:
- F1: The book loses because it is short against coins that rise. It is short on 61 % of days, while the coins drift up by 0.07 to 0.16 % a day. Its gain from the market's own rise is negative on every coin (-0.030 to -0.065 % a day). Its timing (+0.004 to +0.069 % a day on 5 of 6 coins, -0.026 on XRP) does not cover that, so the book earns -0.029 % a day. Per case, the unusual move (+0.58 %, 3.0 times the 0.19 % cost of a trade) is outweighed by the 10-day drift against the short (-1.19 %), which leaves a total move of -0.61 %.
- F2: The forecast's size grades the outcome, and its weak end loses. By |forecast| quartile, the 10-day short-direction total move per case is -2.10 %, -0.45 %, -0.24 % and +1.43 % (809 cases). Per short bar, the daily gain is -0.155 % at |forecast| 0 to 5 (1540 bars), +0.067 % at 5 to 10, +0.167 % at 10 to 15 and +0.243 % at 15 to 21 (1166 bars).
- F3: The book keeps its shorts well past the idea's horizon, and those days lose. Trades last 19.0 days on average against a 10-day horizon. The 989 short bars held after the forecast returned to 0 lose -0.217 % a day. The 2482 short trades average -2.99 % after fees.
