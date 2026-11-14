---
brief: 002_moving-average-cross-trend-persistence
source-idea: N2-06_rebound-in-high-volatility
line: 7.b inconclusive
backtest: N2-06_rebound-in-high-volatility_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 20-day volatility is in the upper half of its last 100 days, the next-day return after a large one-day drop, measured in units of the coin's 20-day volatility, is higher than the coin's average day by more than it is after the same drop in a quiet state.
Consequence: A dip-buyer should size the rebound bet by the volatility state and judge it by the size of the rebound, not by the share of up days, because the gain sits in the size.
Why:
- F1: The test measured direction, but the effect is in size: on top-decile drop bars the coin-netted share of higher next closes is the same in both states (0.102 in high volatility, 0.100 in quiet), yet the mean next-day excess return is 1.11% in high volatility (t 5.28, n 990) against 0.26% in quiet (t 1.57, n 748); so the z of 0.10 hides a fourfold difference in rebound size.
- F2: The gap is not just larger high-volatility swings: scaled by the coin's 20-day volatility, the next-day rebound is 0.17 sd in high volatility (t 4.59, n 854) against 0.02 sd in quiet (t 0.37, n 668).
- F7: The high-volatility rebound appears in every coin, but its strength varies: high-volatility top-decile excess returns run from 0.66% for ETH (t 1.33, n 168) to 1.55% for ZEC (t 2.46, n 163), and BTC is the clearest contrast (1.03%, t 3.11, against −0.25% in quiet).
