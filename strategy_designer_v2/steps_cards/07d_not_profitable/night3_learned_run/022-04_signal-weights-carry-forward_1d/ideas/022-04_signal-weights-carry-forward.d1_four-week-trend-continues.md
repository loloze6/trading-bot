---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-04_signal-weights-carry-forward
line: 7.d not profitable
backtest: 022-04_signal-weights-carry-forward_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The higher a coin's 28-day return, the higher its return over the next 5 days.
Consequence: A trader would lean with a coin's 4-week trend, more the stronger it is, instead of letting a past-year correlation flip the bet against it.
Why:
- F2: The learned weights turn the signals against their own useful direction. The momentum component has the sign of the coin's 28-day return on only 45 % of cases (2432), and the reversal component has the sign of the 1-day move on only 41 % (3117). So the correlation learned over the past 365 days is negative more often than positive.
- F3: Past power does not carry forward. Cases are split by the sign of the past 365-day weight, and the next 5-day excess return is read in the direction of the raw signal. For the 28-day return it is +0.29 % when the past weight was positive (t 0.85, 1091 cases) and +0.31 % when it was negative (t 1.14, 1341 cases). For the 1-day move it is +0.54 % (t 1.76, 1289) against +0.32 % (t 1.29, 1825). The raw signal predicts the same way whichever sign was learned, so a negative learned weight simply bets against it.
- F4: The raw 28-day return predicts the next 5 days in the trend's direction and is graded at its ends. The sign of the 28-day return earns +0.30 % excess per 5-day case (t 1.41, 2432 cases), about 1.6 times a trade's cost. Its top fifth per coin is followed by +1.16 % excess and its bottom fifth by -0.49 %, a spread of 1.66 % (t 2.21, 486 against 490 cases).
- F1: The book's loss comes from its timing, not from the market: it earns -0.0396 % a day, of which only -0.0071 % is the coin's own drift on the position held and -0.0325 % is timing. It is short on 51 % of days and long on 45 %, with a mean position of 0.32 of the book. The forecast's direction earns -0.42 % excess per 5-day case (t -2.26, 3254 cases), which is -2.5 times the 0.19 % cost of a trade.
