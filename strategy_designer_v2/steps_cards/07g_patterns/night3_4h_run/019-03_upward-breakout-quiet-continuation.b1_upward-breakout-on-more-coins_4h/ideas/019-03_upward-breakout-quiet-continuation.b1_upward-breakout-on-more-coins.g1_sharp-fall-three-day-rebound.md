---
brief: 019_quiet-range-then-breakout-on-four-hour-bars
source-idea: 019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins
line: 7.g patterns
backtest: 019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 4h
period: folds A, B, C, D
---
Idea: After a coin's sharp fall over the past day, measured against its own 30-day volatility, the coin rises over the next three days, and the larger that fall, the larger the rise.
Consequence: A trader would buy a coin after an unusually sharp one-day fall rather than sell it, and size the bet larger the sharper the fall, instead of trading quiet-range breakouts.
Why:
- F3: The opposite break pays instead. A 4h close below the prior 2-day low is followed by +1.53 % unusual over 3 days (t 4.4, 753 cases), and the effect is graded by depth in the coin's volatility. From the deepest quartile to the shallowest the moves are +3.98 % (t 4.2), +3.84 % (t 5.9), +1.47 % and −0.53 %. The mean is positive in all 19 coins and in 16 of 24 windows.
- F4: That rebound is a market-wide one. Down-breaks shared by many coins at the same bar are followed by +3.87 % (t 7.3, 320 cases), those by few coins by −1.15 % (t −1.3, 97 cases). Averaged per bar time, the down-break mean is +0.05 % (t 0.07, 164 times), and the coin's move minus the other coins' same-time move is +0.16 % (t 0.66). It also failed in the 2018 bear year (−3.53 %, t −2.2, 37 cases).
- F5: Graded on the 1-day return itself, only the sharpest falls stand out. The lowest decile of the 1-day return, measured in the coin's volatility, is followed by +2.09 % unusual over 3 days (t 7.4, 911 cases). This holds as +1.11 % (t 2.2, 253 bar times) when averaged across coins at the same time, and gives way to ≈0 or negative from the third decile on. The +2.09 % is about 9.5 times the 0.22 % cost of a round trip.
