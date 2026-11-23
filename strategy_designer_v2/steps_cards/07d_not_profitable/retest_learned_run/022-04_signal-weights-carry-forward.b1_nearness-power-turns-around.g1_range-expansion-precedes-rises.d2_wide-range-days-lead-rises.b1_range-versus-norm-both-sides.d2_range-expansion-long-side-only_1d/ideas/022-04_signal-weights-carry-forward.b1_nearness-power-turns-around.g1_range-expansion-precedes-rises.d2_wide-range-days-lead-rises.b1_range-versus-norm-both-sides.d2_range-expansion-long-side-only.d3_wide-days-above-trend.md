---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.d2_range-expansion-long-side-only
line: 7.d confirmed, not profitable
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.d2_range-expansion-long-side-only_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The further a coin's daily high-low range exceeds its average range over the past 30 days, the higher that coin's return over the next 3 days above its usual drift, only while the coin closes above its 50-day mean, with no lean against the coin after narrower days.
Consequence: A trader would buy wide days in proportion to their width only in coins above their 50-day mean, and refuse them below it, where wide days are followed by no rise.
Why:
- F8: On the 3-day grid, the signal's rise sits mostly in the widest days and in coins above their 50-day mean:
- F3: A positive 30-day return is not an effect on its own: grid cases with a positive 30-day return and no signal earn −0.25 % above drift (t −1.16, 1164 cases), and with a positive 60-day return −0.32 % (t −1.15, 788 cases). Only wide days in an up-trending coin carry the move, which fits the theory's trend-following behaviour.
- F1: The Calmar failure comes from one fall: the book's deepest fall is −40.7 % over 164 days from w1 into w2, while the coins fell −64.1%. My approximate rebuild of the book gives the same picture (Sharpe 0.853, deepest fall −39.4 %, Calmar 0.67), and the four losing windows (w1 −18.8 %, w2 −15.7 %, w7 −13.4 %, w14 −22.7 %) are all windows where the coins fell 23–50 %.
