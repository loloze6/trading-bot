---
brief: 025_bounces-fade-in-falling-markets
source-idea: 025-03_bounce-falling-versus-rising-regime
line: 7.d not profitable
backtest: 025-03_bounce-falling-versus-rising-regime_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In one coin, the 5-day return after a one-day rise of several usual daily moves is lower when its 90-day return is negative than when its 90-day return is positive. In the negative case, the shortfall grows the deeper its 30-day return lies below zero in usual daily moves, rather than with the size of the rise.
Consequence: A trader would fade bounces in falling coins harder the deeper the coin's last month's fall, and give little weight to the bounce's size.
Why:
- F1: The short side carries the book's whole loss. Short positions summed −5.08 of bar gain against +12.17 for longs, over 7235 and 8034 bars. Short trades averaged −3.11 % net with a 37.5 % win rate, against +3.93 % net and 48.2 % for longs (2319 and 2510 trades). Fees of 2.74 were then taken from a gross of 7.09.
- F2: Inside short cases, the fade is graded by the coin's own 30-day return (in usual daily moves), not by the rise:
- F4: The rise's size grades the move only on the long side. Long-case gain grows from −0.79 % to +1.79 % (t 2.59) across rise quartiles. On the short side the smallest rises fade most: +1.54 % (t 2.86) in the smallest quartile against +0.46 % in the largest. The tested sizing therefore puts most short weight where the fade is weakest.
- F5: The fade depends on the year, which explains the leave-one-window-out failure:
