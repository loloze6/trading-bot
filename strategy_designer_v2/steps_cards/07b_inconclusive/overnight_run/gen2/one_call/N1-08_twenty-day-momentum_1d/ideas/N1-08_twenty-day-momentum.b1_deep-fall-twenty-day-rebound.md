---
brief: 002_moving-average-cross-trend-persistence
source-idea: N1-08_twenty-day-momentum
line: 7.b inconclusive
backtest: N1-08_twenty-day-momentum_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: After a coin's 20-day return falls deep into the bottom of its recent range, the coin's price rises over the next 20 daily bars by more than its usual 20-bar return.
Consequence: A trader should refuse momentum shorts after deep 20-day falls and treat them as rebound candidates instead.
Why:
- F1: The forward 20-bar excess return is U-shaped across forecast fifths, not a straight line: the bottom fifth (mean forecast -14.9) has +0.040, the middle three fifths have -0.017, -0.026 and -0.020, and the top fifth (mean +17.6) has +0.023 (827 non-overlapping cases, about 165 per fifth). Both extremes beat the middle, so the linear slope cancels to t = 0.05.
- F2: The two sides pull in opposite directions. Long bars have a mean signed forward return of +0.027 (t = 1.67, n = 400). Short bars have -0.023 (t = -2.20, n = 427), so shorting after 20-day falls loses money, and the slope inside the short side is t = -2.65.
- F3: After the deepest falls (forecast ≤ -12) the next 20 bars rise: mean excess return is +0.030 (t = 1.75, n = 124). It is positive for all six coins (+0.010 to +0.057) and in 5 of 8 years (2020: +0.143, t = 4.1, n = 10). Against the cross-coin mean at the same bar it is -0.002 (t = -0.19), so the rebound is market-wide.
