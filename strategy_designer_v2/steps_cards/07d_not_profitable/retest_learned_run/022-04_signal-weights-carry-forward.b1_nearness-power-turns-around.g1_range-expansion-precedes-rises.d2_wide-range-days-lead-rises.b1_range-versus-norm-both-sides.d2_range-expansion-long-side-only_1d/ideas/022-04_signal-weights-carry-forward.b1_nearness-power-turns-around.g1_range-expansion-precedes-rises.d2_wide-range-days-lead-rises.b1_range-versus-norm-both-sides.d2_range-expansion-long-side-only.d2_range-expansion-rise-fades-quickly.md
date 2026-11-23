---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.d2_range-expansion-long-side-only
line: 7.d confirmed, not profitable
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.d2_range-expansion-long-side-only_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The further a coin's daily high-low range exceeds its average range over the past 30 days, the higher that coin's return over the next 3 days above its usual drift, the rise coming within those 3 days and fading once the coin's range is back at its 30-day average, only while the coin's 30-day return is positive.
Consequence: A trader would hold the long only while the day's width stays above its 30-day norm in a rising coin, rather than carrying it through average days, which earn almost nothing.
Why:
- F5: The book spends much of its time in positions the signal no longer supports. Of 11503 held bars, 5211 had a forecast of 0, a leftover of the 3-bar minimum hold and the volatility sizing. Those bars earned +0.028 % each, against +0.243 % on the 6292 bars with a positive forecast.
- F6: Combining the two changes repairs the failing measure in an approximate rebuild with the backtest's cost:
- F2: The effect holds only when the coin's own 30-day return is positive. There, signal grid cases earn +0.82 % above drift over 3 days (t 2.87, 1024 cases). When the 30-day return is negative they earn −0.34 % (t −1.03, 614 cases). The 60-day return splits it the same way: +1.04 % (t 2.73, 639 cases) against −0.42 % (t −1.06, 471 cases).
- F4: When the 30-day return is positive, the effect is graded by the width of the day. By forecast tercile, the excess 3-day return is +0.02 %, +0.35 % and +2.07 % (about 341 cases each). When the 30-day return is negative, the terciles are −0.05 %, −0.64 % and −0.32 %, so no grading at all.
