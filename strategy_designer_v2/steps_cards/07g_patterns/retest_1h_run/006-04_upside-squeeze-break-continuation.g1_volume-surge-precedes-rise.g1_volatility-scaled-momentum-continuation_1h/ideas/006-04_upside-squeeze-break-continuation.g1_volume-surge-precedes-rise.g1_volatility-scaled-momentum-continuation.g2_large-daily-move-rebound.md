---
brief: 006_range-compression-precedes-expansion
source-idea: 006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise.g1_volatility-scaled-momentum-continuation
line: 7.g patterns
backtest: 006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise.g1_volatility-scaled-momentum-continuation_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's 1-day move relative to its own 20-day volatility, in either direction, the more its price rises over the next 3 days relative to its usual 3-day return. The strongest rise follows the sharpest 1-day falls.
Consequence: A sharp 1-day dislocation, especially a fall, is a reason to lean long for the next three days rather than to follow the move.
Why:
- F2: The size of a coin's 1-day move, scaled by its 20-day volatility, predicts its 3-day excess return in a U shape. On the non-overlapping 72-bar grid, the bottom quintile (largest 1-day falls) is followed by +0.0066 (t 2.32, n 939) and the top quintile (largest rises) by +0.0047 (t 1.64). The middle three quintiles give −0.0028 to −0.0046. The Spearman correlation of the absolute scaled 1-day move with the 3-day excess return is positive in all six coins (0.026 to 0.064, about 780 cases each).
- F4: Compression does not precede larger moves, against the brief. The narrowest 5-day high-low range quintile (scaled by 20-day volatility) is followed by a mean absolute 3-day move of 0.0549, about the same as the middle quintiles (0.052 to 0.056). The widest-range quintile is followed by 0.0663, and the highest 1-day-versus-20-day volatility quintile by 0.0619 against 0.0534 for the lowest. Large moves follow large moves, not quiet periods.
