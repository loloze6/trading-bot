---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score
line: 7.d not profitable
backtest: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's 28-day return and its closeness to its 90-day high are combined into one score, each weighted equally in its known direction, the coin's return over the next 5 days is higher the higher that score is.
Consequence: Drop the 1-day reversal and the volatility signal from the combination so that position size follows the two signals that carry the move, raising the gain per unit held.
Why:
- F3: The equal four-signal score dilutes the effect: its product with the 5-day excess return has t 0.81 on 3419 grid cases. Momentum plus nearness to the 90-day high reaches t 2.10, and 28-day momentum alone t 1.95, while minus volatility gives t -0.17 and the 1-day reversal t -1.47, the wrong sign.
- F4: The forecast's 5-day excess return does not rise steadily with the forecast. It is -0.56 % in the -5 to -2 bin, +0.59 % in the 2 to 5 bin and -0.13 % in the 5 to 10 bin (171 cases), so the largest positions are not on the largest moves.
- F8: Size is not the binding limit: the measured move is +0.96 % per case over 5 days (strength 0.082), 5.0 times the 0.19 % round-trip cost. The weak mean return comes from diluting the signal (F3) and from the short side's dead weight (F2).
