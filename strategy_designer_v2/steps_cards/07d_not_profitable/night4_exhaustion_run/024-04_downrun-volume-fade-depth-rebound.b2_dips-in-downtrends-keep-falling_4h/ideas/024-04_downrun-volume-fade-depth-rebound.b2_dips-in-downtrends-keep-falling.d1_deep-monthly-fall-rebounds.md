---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-04_downrun-volume-fade-depth-rebound.b2_dips-in-downtrends-keep-falling
line: 7.d not profitable
backtest: 024-04_downrun-volume-fade-depth-rebound.b2_dips-in-downtrends-keep-falling_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: After a fall over the past 30 days that is large against the coin's usual 30-day move, the coin rises over the next three days. The deeper the 30-day fall against that usual move, the larger the rise.
Consequence: A trader buys, or at least stops shorting, coins after a deep monthly fall, because what follows is a rebound larger than the coin's drift and larger than the cost of a trade.
Why:
- F3: The idea's grading by the 30-day return runs the wrong way at the deep end. Cases with a 30-day return below -25 % have strength -0.107 (t -2.01, 496 cases, -0.82 % unusual move). That is a rebound against the short. Cases between -25 % and -2.4 % have strength +0.07 to +0.10 (t 1.76 to 2.44).
- F4: On the non-overlapping 18-bar grid of all bars, a 30-day return below -25 % is followed by a mean 3-day rise of +1.07 % (t 2.53, 511 cases). A 30-day return between -25 % and -15 % is followed by -0.76 % (t -2.17, 466 cases).
- F1: The book loses because it is short a coin that rises on average: its mean daily return of -0.000227 splits into -0.000694 from the market's own rise and +0.000467 from timing, and it is short on 63 % of coin-days with a mean position of -0.94.
- F2: Per case, the move the bet captures does not cover a trade: the unusual move is +0.20 % (strength 0.025, t 1.53, 3417 cases) against a cost of 0.19 %. After the normal drift of -0.41 % on the short side, the total move is -0.21 %. The 3486 short trades lose -1.91 % gross and -2.01 % net, with 30 % winners.
