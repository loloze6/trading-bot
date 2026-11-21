---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.d1_momentum-and-nearness-score
line: 7.d not profitable
backtest: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.d1_momentum-and-nearness-score_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The further a coin's close sits below its 90-day closing high, the higher the coin's return over the next 5 days.
Consequence: A coin deep below its 90-day high is a reason to buy the rebound, and to refuse to short it.
Why:
- F4: The most negative scores are followed by rises rather than falls. In the lowest forecast decile the coin's next-day return is +0.23 %, against +0.36 % and +0.43 % in the two highest deciles and −0.14 % in decile 2.
- F5: Deep falls below the 90-day high are followed by rebounds.
