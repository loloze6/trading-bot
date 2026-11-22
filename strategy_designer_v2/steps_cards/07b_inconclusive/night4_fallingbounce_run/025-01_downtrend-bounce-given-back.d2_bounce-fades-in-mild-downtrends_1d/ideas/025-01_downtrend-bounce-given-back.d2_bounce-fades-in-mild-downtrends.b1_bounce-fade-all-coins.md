---
brief: 025_bounces-fade-in-falling-markets
source-idea: 025-01_downtrend-bounce-given-back.d2_bounce-fades-in-mild-downtrends
line: 7.b inconclusive
backtest: 025-01_downtrend-bounce-given-back.d2_bounce-fades-in-mild-downtrends_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 90-day return is negative, a one-day rise that is large relative to its usual daily move (its 20-day standard deviation of daily returns) is followed by a fall over the next 5 days, and the shallower the coin's 90-day fall, the larger the fall that follows.
Consequence: A trader would fade bounces in coins drifting gently lower, and refuse to fade bounces in coins that have already crashed, where bounces hold.
Why:
- F1: The main measure is on the side the idea predicts but too small to show: the mean unusual 5-day move after the short bets is +0.23 % (t 0.78, 1,045 cases, 6 coins), only 0.026 of the coin's usual 5-day move of 10.6 %. My recount gives the same, +0.22 % (t 0.74, 1,045 cases).
- F2: The idea's grading by depth holds while its mean does not. Step 5's depth slope is positive (t 2.94). By depth quartile, the deepest-fall quarter of cases gives back nothing: its unusual 5-day move is −1.18 % (t −1.58, 263 cases). The other three quarters all fade: +0.92 % (t 1.78), +0.73 % (t 1.50) and +0.41 % (t 0.79, shallowest).
