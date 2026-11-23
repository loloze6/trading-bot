---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.g1_wide-falling-days-rebound
line: 7.g patterns
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.g1_wide-falling-days-rebound_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: On days a coin closes lower, the closer the close sits to the day's high within that day's high-low range, the higher the coin's return over the next 3 days above its usual drift.
Consequence: A trader would lean long after a down day that closed near its high, more strongly the nearer the high, holding for 3 days.
Why:
- F3: On falling days, where the close sits within the day's range adds information of its own. A pooled regression on the range ratio and the close's location in the range (0 at the low, 1 at the high) gives t 4.95 for the range and t 2.90 for the close location (2397 cases). Falling days that closed in the top fifth of their range were followed by +1.48 % excess over 3 days (t 4.00, 480 cases), against −0.81 % to −0.03 % for the middle fifths.
- F4: In the book, the payoff grows with the size of the forecast. Bars with a forecast in (3, 6] gained +0.173 % per bar (t 5.13, 1110), and bars in (0, 3] gained +0.037 % (t 3.15, 2184). Negative-forecast bars gained +0.004 % to +0.006 % (t ≤ 0.64).
