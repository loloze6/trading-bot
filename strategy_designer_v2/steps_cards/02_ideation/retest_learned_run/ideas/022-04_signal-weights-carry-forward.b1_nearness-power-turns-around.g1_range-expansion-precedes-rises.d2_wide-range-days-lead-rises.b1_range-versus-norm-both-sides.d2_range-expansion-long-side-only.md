---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides
line: 7.d confirmed, not profitable
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The further a coin's daily high-low range exceeds its average range over the past 30 days, the higher that coin's return over the next 3 days above its usual drift, with no lean against the coin after narrower days.
Consequence: A trader would take only the long side after wide days, sized with the width, and drop the short side, which earns nothing and pays fees.
Why:
- F1: The short side does not pay for itself: summed bar gains of short positions were -0.004 in falling 30-day markets and -0.19 in rising ones, against fees of -0.23 and -0.16; long positions earned +1.27 and +2.52 against fees of -0.28 and -0.21; narrower-than-norm cases had a 3-day excess of only -0.16 % (t -1.16, n 3570), while wider cases had +0.26 % (t 1.40, n 2153).
- F5: The book was in a position on 99 % of coin-days, mostly with small positions near a zero forecast (mean |allocation| 0.09–0.11 for |f| < 1.5, 14 % of bars with |f| < 0.5). That is why the mean on days in a position is 0.016 % against the required 0.05 %, while the bars with f > 3 carried +2.34 of the +3.6 summed gain.
