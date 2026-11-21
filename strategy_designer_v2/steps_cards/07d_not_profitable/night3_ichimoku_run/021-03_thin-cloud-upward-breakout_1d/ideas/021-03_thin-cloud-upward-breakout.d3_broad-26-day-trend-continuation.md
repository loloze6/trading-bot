---
brief: 021_ichimoku-cloud-as-a-watched-equilibrium
source-idea: 021-03_thin-cloud-upward-breakout
line: 7.d not profitable
backtest: 021-03_thin-cloud-upward-breakout_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's 26-day return, the more the coin rises over the next 26 days.
Consequence: A trader would stay long through a broad rising trend instead of only after the rare cloud cross, holding a position far more of the time.
Why:
- F1: The book's low mean daily return (0.00044 against the 0.0005 needed) comes mostly from how little it holds: it is invested on only 21 % to 33 % of bars per coin (BTC 21 %, ZEC 33 %), with a mean absolute allocation of 0.12 to 0.20, even though each trade earns +6.7 % net on average (336 trades, median +1.6 %). Cost is not the cause: the total move per case is 48.9 times the 0.19 % round trip.
- F4: The coin's 60-day return before the cross sorts the outcome. Trades in its top tercile net +18.7 % against +2.0 % in its bottom tercile (161 trades). Their 26-day forward return is +27.0 % against -0.1 %. The 40-day return sorts the same way more weakly (+10.2 % against +5.8 %, rho 0.155, 208 trades).
- F7: Across all bars, being above the 52-day range midpoint is followed by a modestly better 26-day unusual return. Above, it is +3.7 % (140 non-overlapping cases); below, it is -1.7 % (146). The graded quintiles are noisy: the top-minus-bottom t is -0.62 by position against the 52-day midpoint, 1.35 by position against the 26-day midpoint, and 1.54 by the prior 26-day return.
