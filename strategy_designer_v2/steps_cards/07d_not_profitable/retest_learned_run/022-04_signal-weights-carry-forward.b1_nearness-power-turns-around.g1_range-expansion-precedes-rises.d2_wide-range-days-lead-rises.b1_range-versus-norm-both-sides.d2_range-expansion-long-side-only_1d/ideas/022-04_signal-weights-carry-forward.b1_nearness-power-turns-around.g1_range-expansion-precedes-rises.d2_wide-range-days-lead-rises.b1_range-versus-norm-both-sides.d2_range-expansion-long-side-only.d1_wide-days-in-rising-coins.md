---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.d2_range-expansion-long-side-only
line: 7.d confirmed, not profitable
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.d2_range-expansion-long-side-only_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The further a coin's daily high-low range exceeds its average range over the past 30 days, the higher that coin's return over the next 3 days above its usual drift, only while the coin's own 30-day return is positive, with no lean against the coin after narrower days.
Consequence: A trader would buy after wide days, sized with the width, only in coins that are up over the past 30 days, and stay out after wide days in falling coins, where the rise does not follow.
Why:
- F1: The Calmar failure comes from one fall: the book's deepest fall is −40.7 % over 164 days from w1 into w2, while the coins fell −64.1%. My approximate rebuild of the book gives the same picture (Sharpe 0.853, deepest fall −39.4 %, Calmar 0.67), and the four losing windows (w1 −18.8 %, w2 −15.7 %, w7 −13.4 %, w14 −22.7 %) are all windows where the coins fell 23–50 %.
- F2: The effect holds only when the coin's own 30-day return is positive. There, signal grid cases earn +0.82 % above drift over 3 days (t 2.87, 1024 cases). When the 30-day return is negative they earn −0.34 % (t −1.03, 614 cases). The 60-day return splits it the same way: +1.04 % (t 2.73, 639 cases) against −0.42 % (t −1.06, 471 cases).
- F3: A positive 30-day return is not an effect on its own: grid cases with a positive 30-day return and no signal earn −0.25 % above drift (t −1.16, 1164 cases), and with a positive 60-day return −0.32 % (t −1.15, 788 cases). Only wide days in an up-trending coin carry the move, which fits the theory's trend-following behaviour.
- F4: When the 30-day return is positive, the effect is graded by the width of the day. By forecast tercile, the excess 3-day return is +0.02 %, +0.35 % and +2.07 % (about 341 cases each). When the 30-day return is negative, the terciles are −0.05 %, −0.64 % and −0.32 %, so no grading at all.
- F6: Combining the two changes repairs the failing measure in an approximate rebuild with the backtest's cost:
- F7: The 30-day filter does not save the worst windows completely. In w1, w2, w7 and w14 the held bars lost in all four groupings of 30-day sign and forecast sign (mean gain per held bar −0.14 % to −0.29 %). The filter shrinks the falls by holding less often, and does not turn those windows positive.
