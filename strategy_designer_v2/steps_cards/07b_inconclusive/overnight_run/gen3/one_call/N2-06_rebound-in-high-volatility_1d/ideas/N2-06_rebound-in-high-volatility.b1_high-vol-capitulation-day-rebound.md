---
brief: 002_moving-average-cross-trend-persistence
source-idea: N2-06_rebound-in-high-volatility
line: 7.b inconclusive
backtest: N2-06_rebound-in-high-volatility_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 20-day volatility is in the upper half of its last 100 days, a large one-day drop that closes a 5-day fall of more than 10% is followed by a next-day rise larger than the coin's average day, and larger than after the same kind of drop when volatility is quiet.
Consequence: A trader buying the dip should keep it for high-volatility days that extend a multi-day slide, and pass on lone drops and on quiet-volatility drops.
Why:
- F1: The test measured direction, but the effect is in size: on top-decile drop bars the coin-netted share of higher next closes is the same in both states (0.102 in high volatility, 0.100 in quiet), yet the mean next-day excess return is 1.11% in high volatility (t 5.28, n 990) against 0.26% in quiet (t 1.57, n 748); so the z of 0.10 hides a fourfold difference in rebound size.
- F3: The effect sits in drops that extend a multi-day fall: when the 5-day return is below −10%, top-decile drops in high volatility rebound 2.32% the next day (t 4.98, n 327, net up share 0.163); in quiet bars they rebound 0.06% (t 0.19, n 233); without such a fall the two states are close (0.50% t 2.19 n 527 vs 0.33% t 1.61 n 435).
- F4: The strongest cases are drops where the 5-day fall is 1.5 to 2.5 of the coin's 5-day volatility: in high volatility the next day returns 4.96% (t 6.33, n 135, net up share 0.25), while the same depth in quiet bars returns −0.66% (t −1.59, n 158).
- F6: The rebound grows with the size of the drop. Over all positive forecasts, the next-day excess return rises steadily from −0.15% in the lowest quintile to 0.72% in the highest (t 5.09, n 1695), and within the top decile the high-volatility rebound is largest in its top quarter: 1.64% (t 3.11, n 253).
