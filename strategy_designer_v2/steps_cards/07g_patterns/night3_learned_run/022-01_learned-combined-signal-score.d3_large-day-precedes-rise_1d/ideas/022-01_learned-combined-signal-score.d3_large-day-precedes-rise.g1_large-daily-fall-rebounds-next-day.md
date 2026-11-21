---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-01_learned-combined-signal-score.d3_large-day-precedes-rise
line: 7.g patterns
backtest: 022-01_learned-combined-signal-score.d3_large-day-precedes-rise_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's fall over its last day, measured against its usual daily move over the past 60 days, the higher its return over the next day.
Consequence: After an unusually large down day, lean long the coin for the following day, more the deeper the fall; after a small fall, do not.
Why:
- F1: On daily bars a coin's 1-day return, scaled by its usual daily move, is followed by a reversal the next day. The top third of scaled returns is followed by -0.13 % excess and the bottom third by +0.29 %: top minus bottom -0.42 %, Welch t -4.11, on 14356 non-overlapping cases. The Spearman rho is -0.082, and it is negative in both halves of the windows (w1-12: -0.110 on 7174 cases; w13-24: -0.059 on 7182).
- F2: The next-day reversal is graded inside down days only. Among down days, the largest third of falls is followed by +0.53 % excess next day against -0.05 % for the smallest third (difference +0.59 %, Welch t 4.13, rho 0.078, 7056 cases). Among up days the largest third against the smallest differs by only +0.11 % (t 0.84, 7286 cases). The largest falls' fifth is followed by +0.50 %, about 2.6 times the 0.19 % this backtest charged for a round trip.
