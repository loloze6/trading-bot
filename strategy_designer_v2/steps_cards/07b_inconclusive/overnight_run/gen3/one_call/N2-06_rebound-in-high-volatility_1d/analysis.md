---
line: 7.b inconclusive
backtest: N2-06_rebound-in-high-volatility_1d
idea tested: N2-06_rebound-in-high-volatility
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.2991 USD
---
## Findings
- **F1:** The test measured direction, but the effect is in size: on top-decile drop bars the coin-netted share of higher next closes is the same in both states (0.102 in high volatility, 0.100 in quiet), yet the mean next-day excess return is 1.11% in high volatility (t 5.28, n 990) against 0.26% in quiet (t 1.57, n 748); so the z of 0.10 hides a fourfold difference in rebound size.
- **F2:** The gap is not just larger high-volatility swings: scaled by the coin's 20-day volatility, the next-day rebound is 0.17 sd in high volatility (t 4.59, n 854) against 0.02 sd in quiet (t 0.37, n 668).
- **F3:** The effect sits in drops that extend a multi-day fall: when the 5-day return is below −10%, top-decile drops in high volatility rebound 2.32% the next day (t 4.98, n 327, net up share 0.163); in quiet bars they rebound 0.06% (t 0.19, n 233); without such a fall the two states are close (0.50% t 2.19 n 527 vs 0.33% t 1.61 n 435).
- **F4:** The strongest cases are drops where the 5-day fall is 1.5 to 2.5 of the coin's 5-day volatility: in high volatility the next day returns 4.96% (t 6.33, n 135, net up share 0.25), while the same depth in quiet bars returns −0.66% (t −1.59, n 158).
- **F5:** The effect varies a lot across periods. Deep drops (5-day z below −1.5) return 5.70% in w13–18 (t 5.85, n 94) and 1.35% in w19–24 (t 2.29, n 88), but only 0.19% (t 0.26, n 78) in w1–6 and 0.34% (t 0.53, n 86) in w7–12; by year, 2025 shows nothing in either state (0.16%, t 0.28, n 112 in high volatility).
- **F6:** The rebound grows with the size of the drop. Over all positive forecasts, the next-day excess return rises steadily from −0.15% in the lowest quintile to 0.72% in the highest (t 5.09, n 1695), and within the top decile the high-volatility rebound is largest in its top quarter: 1.64% (t 3.11, n 253).
- **F7:** The high-volatility rebound appears in every coin, but its strength varies: high-volatility top-decile excess returns run from 0.66% for ETH (t 1.33, n 168) to 1.55% for ZEC (t 2.46, n 163), and BTC is the clearest contrast (1.03%, t 3.11, against −0.25% in quiet).

## Ideas
- `N2-06_rebound-in-high-volatility.b1_high-vol-capitulation-day-rebound` (from F1, F3, F4, F6): In a coin whose 20-day volatility is in the upper half of its last 100 days, a large one-day drop that closes a 5-day fall of more than 10% is followed by a next-day rise larger than the coin's average day, and larger than after the same kind of drop when volatility is quiet.
- `N2-06_rebound-in-high-volatility.b2_volatility-scaled-rebound-size` (from F1, F2, F7): In a coin whose 20-day volatility is in the upper half of its last 100 days, the next-day return after a large one-day drop, measured in units of the coin's 20-day volatility, is higher than the coin's average day by more than it is after the same drop in a quiet state.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
