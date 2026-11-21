---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-04_signal-weights-carry-forward
line: 7.d not profitable
backtest: 022-04_signal-weights-carry-forward_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's move over the last day, the larger its move in the same direction over the next 5 days.
Consequence: A trader would treat a large daily move as the start of a short continuation and refuse to fade it.
Why:
- F5: The last day's move is followed by more of the same, not by a reversal. Its sign earns +0.41 % excess over the next 5 days (t 2.13, 3117 cases), and its top fifth is followed by +1.05 %. The grading is uneven, though: the second-lowest fifth is followed by -1.58 % and the lowest by +0.43 %. Of the brief's four signals, only these two raw continuation signals have a move per case larger than a trade's cost.
- F2: The learned weights turn the signals against their own useful direction. The momentum component has the sign of the coin's 28-day return on only 45 % of cases (2432), and the reversal component has the sign of the 1-day move on only 41 % (3117). So the correlation learned over the past 365 days is negative more often than positive.
- F3: Past power does not carry forward. Cases are split by the sign of the past 365-day weight, and the next 5-day excess return is read in the direction of the raw signal. For the 28-day return it is +0.29 % when the past weight was positive (t 0.85, 1091 cases) and +0.31 % when it was negative (t 1.14, 1341 cases). For the 1-day move it is +0.54 % (t 1.76, 1289) against +0.32 % (t 1.29, 1825). The raw signal predicts the same way whichever sign was learned, so a negative learned weight simply bets against it.
