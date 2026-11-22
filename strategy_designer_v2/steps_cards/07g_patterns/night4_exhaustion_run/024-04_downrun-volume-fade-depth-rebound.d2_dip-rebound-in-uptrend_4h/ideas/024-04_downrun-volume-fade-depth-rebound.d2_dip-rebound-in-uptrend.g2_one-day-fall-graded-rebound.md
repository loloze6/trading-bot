---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-04_downrun-volume-fade-depth-rebound.d2_dip-rebound-in-uptrend
line: 7.g patterns
backtest: 024-04_downrun-volume-fade-depth-rebound.d2_dip-rebound-in-uptrend_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: The larger a coin's 1-day fall measured in its usual 4-hour moves over the past 30 days, the larger its rise over the next day.
Consequence: A trader would buy the deepest one-day drops for a one-day rebound, sized by how deep the drop is in usual moves.
Why:
- F2: Large one-day falls are followed by a graded rebound with no streak and no 30-day regime needed. On the 6-bar grid, the decile with the deepest 1-day fall (below −3.99 usual moves) rose +0.62 % above drift over the next day (t 4.25, 1522 cases), the next decile rose +0.25 % (t 2.00), and the other deciles sat between −0.25 % and 0.00 %; Spearman rho is −0.098 (p < 0.0001, n 7473) among falls and −0.019 (p 0.10) among rises.
- F4: On the 18-bar grid, the deepest decile of the current streak's loss in usual moves rebounded +1.02 % (t 2.42, 501 cases). With the 180-bar return above 0 the deepest fifth gave +1.53 % (t 3.37, 437 cases); with it below 0 the deepest fifth gave only +0.49 % (t 1.17, 420 cases). This is the tested idea's own effect, and it is concentrated in the deep tail.
