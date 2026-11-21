---
brief: 020_support-and-resistance-at-past-turning-prices
source-idea: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.d2_tight-cluster-of-broken-lows
line: 7.d not profitable
backtest: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.d2_tight-cluster-of-broken-lows_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's daily close sits just below prices where it turned up several times in the past 90 days, it tends to fall over the next 5 days, only while its 60-day decline is still mild. The more such past turning-up lows lie within a few percent above the close, the nearer the closest of them, and the smaller the coin's 60-day loss, the larger the fall.
Consequence: A short on a broken support is worth taking early in a decline and should be refused after a deep 60-day fall, when the coin tends to rebound instead.
Why:
- F5: Among bars with a past low above the close, the coin's past 60-day return shapes the 5-day move:
- F2: Even where the short signal was strongest, the coin barely fell, so a short on this idea cannot cover the 0.19 % cost of a trade.
- F4: Once the standardisation is removed, the raw count-times-nearness measure grades the move only weakly. Its slope on the 5-day excess return has t -1.14 (2359 cases). Its quartiles give +1.13 %, -0.32 %, +0.24 % and -0.10 % raw.
