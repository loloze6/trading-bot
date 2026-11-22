---
brief: 025_bounces-fade-in-falling-markets
source-idea: 025-01_downtrend-bounce-given-back
line: 7.g patterns
backtest: 025-01_downtrend-bounce-given-back_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 90-day return is positive, a one-day rise that is large relative to its usual daily move (its 20-day standard deviation of daily returns) is followed by a further rise over the next 5 days, and the larger that rise in units of the usual daily move, the larger the further rise.
Consequence: A sharp up day in a coin already rising over the past months is a reason to buy it, or to refuse to short it, over the following days.
Why:
- F1: In coins whose 90-day return is not negative (the regime the strategy left flat), a one-day rise is followed by a 5-day move that grows with its size in usual daily moves. Over 751 non-overlapping up days the Spearman correlation between the scaled rise and the coin's scaled unusual 5-day move is 0.134 (p = 0.0002). Rises of 1.5 to 2.5 usual moves are followed by +2.9 % (t 2.24, n 90), and rises above 2.5 by +6.9 % (t 1.70, n 26).
- F2: That continuation after rises in rising coins has a positive correlation in all six coins: 0.157 BTC, 0.161 ETH, 0.044 LTC, 0.060 XMR, 0.152 XRP and 0.241 ZEC. Rises above 1.5 usual moves are followed by a positive mean unusual 5-day move in every coin, from +0.1 % (LTC) to +10.0 % (XRP).
- F3: Large rises (above 1.5 usual moves) are followed by a 5-day unusual move 5.8 % higher in rising coins than in falling coins (Welch t 3.53; 116 against 68 cases). This is the contrast the brief names as its test.
