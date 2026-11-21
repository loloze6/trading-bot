---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.d3_combined-score-in-uptrends
line: 7.d not profitable
backtest: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.d3_combined-score-in-uptrends_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's four signals are combined into one score, the coin's return over the next 5 days is higher the higher that score is, only while its 28-day return is up, and there the rise is larger the stronger the score, with the 28-day return carrying most of the score's weight in place of nearness to the 90-day high and low 30-day volatility.
Consequence: In a rising month, a trader would stop shorting coins near their highs or with calm prices and lean long in proportion to the month's rise.
Why:
- F1: The book's loss comes almost entirely from its short positions in the "trending" regime. There they lost 25.0 bps per bar over 4745 bars, against +3.4 bps per bar for its 3343 long bars. Outside that regime, shorts lost 2.4 bps over 1442 bars and longs gained 2.8 bps over 1587 bars.
- F3: Inside the gate (28-day return up), the learned score was short on 57 % of bars. Its rank correlation is -0.24 with nearness to the 90-day high and -0.19 with negative 30-day volatility, but only +0.09 with 28-day momentum. In a rising month, the learned weights therefore bet against coins near their highs and against calm coins.
- F4: Those bets point the wrong way. On non-overlapping 5-day cases in the gate, the score's short cases had an excess return of +0.78 % (t 2.03, 961 cases) and its long cases -0.40 % (t -0.91, 701 cases). The slope on the score was negative (t -1.15, 1662 cases), so the learned combination does not carry forward to unseen dates.
- F6: In the gate, the coin itself rose over the next 5 days, more so in the upper half of its 28-day rise. By quartile of the 28-day return (lowest to highest), the total 5-day move was +0.61 % (t 1.19), -0.16 %, +1.89 % (t 2.78) and +1.49 % (t 2.20), with 320 to 325 cases each. The upper two quartiles' moves are about 8 to 10 times a 0.19 % round trip.
- F7: Over all bars, the top fifth of the 28-day return was followed by a +1.11 % excess 5-day return (t 1.98, 490 cases). The 28-day return's correlation with the next 5-day excess return was +0.041 (t 2.01, 2450 cases). Of the four signals, only momentum carries a positive and roughly consistent effect.
