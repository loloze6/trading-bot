---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.d3_combined-score-in-uptrends
line: 7.d not profitable
backtest: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.d3_combined-score-in-uptrends_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's 28-day return is up, its return over the next 5 days is higher the larger that 28-day rise.
Consequence: A trader would hold a coin long during a rising month, with more exposure the stronger the month's rise, and take no short against it.
Why:
- F1: The book's loss comes almost entirely from its short positions in the "trending" regime. There they lost 25.0 bps per bar over 4745 bars, against +3.4 bps per bar for its 3343 long bars. Outside that regime, shorts lost 2.4 bps over 1442 bars and longs gained 2.8 bps over 1587 bars.
- F2: The shorts lost in 7 of the 8 years: -13 to -39 bps per bar in 2019-2021 and 2023-2025, and +4.8 in 2018 and +30.1 in 2022. The longs lost only in 2018 (-16.0) and 2023 (-8.4) and gained up to +11.8 bps in 2024. So the failure holds in almost every period, which matches the failed leave-one-window-out Sharpe of -1.24.
- F6: In the gate, the coin itself rose over the next 5 days, more so in the upper half of its 28-day rise. By quartile of the 28-day return (lowest to highest), the total 5-day move was +0.61 % (t 1.19), -0.16 %, +1.89 % (t 2.78) and +1.49 % (t 2.20), with 320 to 325 cases each. The upper two quartiles' moves are about 8 to 10 times a 0.19 % round trip.
- F7: Over all bars, the top fifth of the 28-day return was followed by a +1.11 % excess 5-day return (t 1.98, 490 cases). The 28-day return's correlation with the next 5-day excess return was +0.041 (t 2.01, 2450 cases). Of the four signals, only momentum carries a positive and roughly consistent effect.
