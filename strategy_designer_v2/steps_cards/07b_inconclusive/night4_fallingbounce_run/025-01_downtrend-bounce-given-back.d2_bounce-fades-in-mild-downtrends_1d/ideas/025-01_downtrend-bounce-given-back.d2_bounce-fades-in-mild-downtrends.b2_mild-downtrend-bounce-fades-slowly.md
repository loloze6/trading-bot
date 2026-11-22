---
brief: 025_bounces-fade-in-falling-markets
source-idea: 025-01_downtrend-bounce-given-back.d2_bounce-fades-in-mild-downtrends
line: 7.b inconclusive
backtest: 025-01_downtrend-bounce-given-back.d2_bounce-fades-in-mild-downtrends_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 90-day return is negative, a one-day rise that is large relative to its usual daily move (its 20-day standard deviation of daily returns) is followed by a fall over the next 10 days, and the shallower the coin's 90-day fall, the larger the fall that follows.
Consequence: A trader would fade sharp bounces in gently falling coins over about two weeks, not one, and would refuse to fade them in coins that have already crashed.
Why:
- F2: The idea's grading by depth holds while its mean does not. Step 5's depth slope is positive (t 2.94). By depth quartile, the deepest-fall quarter of cases gives back nothing: its unusual 5-day move is −1.18 % (t −1.58, 263 cases). The other three quarters all fade: +0.92 % (t 1.78), +0.73 % (t 1.50) and +0.41 % (t 0.79, shallowest).
- F3: Over 10 days the fade in the three shallower quarters is larger: +2.21 % (t 2.75, 242 cases), +0.06 % (t 0.06) and +1.76 % (t 2.14, shallowest). The deepest quarter loses −1.75 % (t −1.78, 259 cases). Over all cases, the 10-day move is +0.55 % (t 1.21) against the plan's 5-day +0.22 % (t 0.74).
