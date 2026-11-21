---
brief: 019_quiet-range-then-breakout-on-four-hour-bars
source-idea: 019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins
line: 7.g patterns
backtest: 019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 4h
period: folds A, B, C, D
---
Idea: When a coin's four-hour bar closes below the lowest low of its preceding two days, the coin rises over the next three days, and the deeper that close lies below the low, measured in the coin's 30-day volatility, the larger the rise.
Consequence: A downside break of a two-day range is a reason to buy the coin and not to sell it, all the more as the break is deep.
Why:
- F1: The tested upward breakout adds little on this data: on the 18-bar grid, bars that close above the prior 2-day high are followed by an unusual 3-day move of +0.12 % (t 0.63, 831 cases), and the breakout's size does not grade it (quartiles +0.30, −1.27, +0.46, +1.04 %).
- F2: The brief's premise that narrow stretches lead to larger moves fails here: the 3-day absolute move, in units of the coin's usual move, is 0.66 after the narrowest fifth of 2-day stretches and 0.73 after the widest, and the narrowest fifth is followed by −0.72 % unusual (t −3.1, 1829 cases; −0.33 %, t −0.97 over 515 bar times when averaged across coins at the same time).
- F3: The opposite break pays instead. A 4h close below the prior 2-day low is followed by +1.53 % unusual over 3 days (t 4.4, 753 cases), and the effect is graded by depth in the coin's volatility. From the deepest quartile to the shallowest the moves are +3.98 % (t 4.2), +3.84 % (t 5.9), +1.47 % and −0.53 %. The mean is positive in all 19 coins and in 16 of 24 windows.
- F4: That rebound is a market-wide one. Down-breaks shared by many coins at the same bar are followed by +3.87 % (t 7.3, 320 cases), those by few coins by −1.15 % (t −1.3, 97 cases). Averaged per bar time, the down-break mean is +0.05 % (t 0.07, 164 times), and the coin's move minus the other coins' same-time move is +0.16 % (t 0.66). It also failed in the 2018 bear year (−3.53 %, t −2.2, 37 cases).
