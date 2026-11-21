---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.d3_combined-score-in-uptrends
line: 7.g patterns
backtest: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.d3_combined-score-in-uptrends_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The higher a coin's 28-day return, the higher its return over the next 5 days, and the rise is largest for the coins whose past month rose the most.
Consequence: In a coin whose month has risen strongly, a trader should lean long with the trend and refuse shorts taken against it.
Why:
- F1: The book lost on its shorts and earned on its longs. The 2191 SHORT trades lost 6.52 % each on average before fees (6.62 % after), and the 1579 LONG trades earned 3.20 % (3.10 % after), both held about 10.5 days. Since the forecast is zero outside rising months, almost every short was taken against a coin whose 28-day return was up.
- F2: Inside the rising-month bars, the combined score is not graded the way the idea says. Across its quintiles (333 cases each), the unusual 5-day move was +0.52 %, +1.56 %, +0.44 %, -1.36 % and +0.24 % from most negative to most positive score. The pooled slope per standard deviation was -0.039 (t -1.47, 1662 cases), and five of six coins had a negative t (from -1.38 to -0.31; ZEC +0.15).
- F3: The coin's own 28-day return points the other way from the score. The top quintile of 28-day return (mean +48 %) was followed by an unusual 5-day move of +1.11 % (t 2.09, 490 cases), while the bottom two quintiles had -0.46 % and -0.63 %. The pooled slope per standard deviation was +0.032 (t 1.61, 2450 cases), so a 28-day trend is something to follow rather than to fade with the score. The move in the top quintile is about 5.8 times the 0.19 % cost of a trade.
