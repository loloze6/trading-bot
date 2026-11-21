---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.b1_fixed-weight-score-all-coins
line: 7.d not profitable
backtest: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.b1_fixed-weight-score-all-coins_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's signals are combined into one score, its return over the next 5 days is higher the higher the score, but only its 28-day return and its closeness to its 90-day high are kept. The other two signals, minus its last 1-day return and minus its 30-day volatility, are given no weight, so the rise grows with how strong its recent trend is and how near it trades to its high.
Consequence: A trader should size on trend and nearness to the high alone, since the reversal and calm parts weaken the forecast and shrink the position the book can hold.
Why:
- F1: The book fails on mean daily return (0.000301, against a floor of 0.0005), and the reason is that it is barely invested. Its mean absolute allocation is 0.16 of the book, and it is short 50 % of bars and long 47 %, so its net position is near zero (mean allocation +0.004). Holding the coins earned 0.00134 a day, 4.5 times the book.
- F5: Two of the four signals carry the edge and the other two dilute it. On the 7128 non-overlapping 5-day cases, the score-times-excess-return t is 3.37 for 28-day momentum and 1.85 for nearness to the 90-day high. It is −0.99 for 1-day reversal (the wrong sign) and −0.21 for low volatility.
- F6: Momentum and nearness together predict better than the full score. Their average alone has t 3.63, against 2.82 for the four-signal forecast (7128 cases; correlation between the two scores 0.78).
- F8: Low volatility is not graded. Excess 5-day return by volatility-score quintile runs +0.48 %, −0.07 %, −0.30 %, −0.73 %, +0.62 %, so the calm signal adds noise rather than a graded effect.
