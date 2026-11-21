---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-02_combination-beats-best-single.d1_combination-only-in-downtrends
line: 7.d not profitable
backtest: 022-02_combination-beats-best-single.d1_combination-only-in-downtrends_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's return over the next 5 days lines up more closely with its relearned combined score of its 28-day return, last 1-day return, closeness to its 90-day high and 30-day volatility than with the score of whichever single signal has predicted best, only while its 90-day return is positive, and the more positive that 90-day return the closer the fit.
Consequence: The combined score's bets should be taken on coins in a 90-day rise, where its components carry their usual direction, and not in the declines where it lost through shorts.
Why:
- F1: The book loses through its shorts. Short trades lost 1.90 % net per trade over 1699 trades, against +0.86 % for 1766 longs. Short bars summed −5.18 of gain against +2.82 for long bars, so the book's mean daily return is −0.019 % (Sharpe −0.35) against holding's +0.117 % (Sharpe 0.55).
- F2: The combined score predicts nothing in declines. Its bets' unusual move over 5 days is −0.11 % per case (strength −0.006, 1423 cases), below the 0.19 % cost of a trade. By side it is +0.04 % for shorts (t 0.12, 764 cases) and −0.34 % for longs (t −0.98, 786). Its forecast quintiles are not ordered: +0.19 %, −0.18 %, −0.35 %, −1.04 %, +0.43 %.
- F3: In declines the relearned score is nearly unrelated to the signals it combines. Its Spearman correlation with the 28-day return is −0.065, with the 1-day reversal +0.089, with closeness to the 90-day high −0.083 and with the 30-day volatility −0.043. The weights learned over the past 365 days do not carry into these bars.
- F6: While the 90-day return is positive, momentum holds and is large next to the cost. The top 28-day-return quintile minus the bottom is +2.98 % over 5 days (t 2.82, about 255 cases each). Betting with the sign of the 28-day return gives an unusual move of +0.91 % (t 2.90) and a total move of +1.19 % (t 3.80) over 1272 cases, with a strength of 0.086. That is 4.8 and 6.3 times the 0.19 % cost.
