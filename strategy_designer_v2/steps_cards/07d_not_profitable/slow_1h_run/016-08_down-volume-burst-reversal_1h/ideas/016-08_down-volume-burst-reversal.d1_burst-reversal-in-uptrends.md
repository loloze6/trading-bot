---
brief: 016_grind-versus-jump-moves
source-idea: 016-08_down-volume-burst-reversal
line: 7.d not profitable
backtest: 016-08_down-volume-burst-reversal_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin has fallen over the past 3 days, only while its 30-day return is positive, the larger the share of that period's volume traded in its few busiest hours, the more of the fall the coin wins back over the next 3 days.
Consequence: A trader buys volume-burst dips only inside a rising month, and refuses them when the month is falling and dips keep going.
Why:
- F2: The tested situation predicts the wrong direction on average. After a 72-bar fall, the coin's excess 72-bar forward return is -0.0019 (n=2669). After a rise it is +0.0018 (n=2870), Welch t -1.64. Falls continued rather than reversed.
- F3: The forecast barely ranks the outcome. The Spearman correlation of forecast with excess forward return is 0.029 in 30-day downtrends (n=1181) and 0.035 in 30-day uptrends (n=854), and the verdict's top-minus-bottom difference is only 0.0033 (Welch t 1.05).
- F5: The 30-day trend splits the result. 3-day falls inside a rising 30-day trend were followed by +0.0032 excess (n=854), and falls inside a falling 30-day trend by -0.0041 (t -1.73, n=1181). The book's held days lost -0.00093 a day (Sharpe -0.85, n=5642) in 30-day downtrends against -0.00039 (n=2673) in uptrends.
- F7: The losses gather in bear years. Excess return after falls was -0.025 in 2018 (n=402) and -0.0068 in 2022 (n=344), against +0.003 to +0.009 in 2019 to 2021 and +0.005 in 2025.
