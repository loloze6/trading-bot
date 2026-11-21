---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.b1_fixed-weight-score-all-coins
line: 7.d not profitable
backtest: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.b1_fixed-weight-score-all-coins_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: The higher a coin's 28-day return and the closer its close to its 90-day high, the more the coin rises over the next 10 days.
Consequence: A trader should hold a long position longer and larger the stronger the coin's trend and the nearer it trades to its high, since that is where the book's gain lies and the move outlasts five days.
Why:
- F2: The shorts carry about half the book's time but almost none of its gain. Short bars add 0.000028 of the 0.000322 gross gain per bar, against 0.000293 from long bars. Short trades average +0.10 % net (5081 trades), long trades +7.79 % net (5610 trades).
- F4: The negative-score cases are not falls in total. Coins still rose +0.36 % over 5 days after them (3523 cases), against +1.15 % after positive scores. Most of what a short captures is the unusual move (−0.40 %), not a decline, so the short side's total move is small next to the 0.22 % round trip.
- F7: Momentum plus nearness separates mainly at its upper half. The two top quintiles of the momentum-plus-nearness score are followed by +0.78 % and +0.97 % excess over 5 days (total +1.55 % and +1.73 %). The three lower quintiles are followed by −0.37 % to −0.71 %, while still rising +0.08 % to +0.35 % in total.
- F9: The idea's size covers its cost: its unusual move per case is +0.93 % over 5 days, 4.1 times the 0.22 % round trip (strength 0.072). The book's trades last 10 to 11 days, about twice the 5-day horizon, in line with earlier runs' finding that continuation moves outlast their stated horizon (findings F9, F11).
