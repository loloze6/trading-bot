---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-02_combination-beats-best-single.d1_combination-only-in-downtrends.d1_combination-only-in-uptrends
line: 7.d not profitable
backtest: 022-02_combination-beats-best-single.d1_combination-only-in-downtrends.d1_combination-only-in-uptrends_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's return over the next 5 days lines up more closely with its relearned combined score of its 28-day return, last 1-day return, closeness to its 90-day high and 30-day volatility than with the score of whichever single signal has predicted best, only while its 90-day return is positive and the combined score points the same way as its 28-day return, and the more positive that 90-day return the closer the fit.
Consequence: A trader takes the combined score's bets only when they follow the coin's 28-day direction, which drops the shorts that carried the book's loss.
Why:
- F1: The book's loss comes from its shorts. Short positions summed −10.46 of daily position gain, against +1.16 for longs. The 2189 short trades lost 5.95 % each on average after fees, while the 1638 long trades gained 1.96 %.
- F2: The combined score points the wrong way inside the 90-day rise. Its rank correlation with the next 5-day unusual move is −0.055 (p 0.023, 1704 cases). The 57 % of cases where it was short were followed by +0.85 % (t 2.14), and the cases where it was long by −0.73 % (t −1.80). That is why the idea's size is −0.43 % per case, 2.2 times the 0.19 % cost and of the wrong sign.
- F4: The weights do not carry forward from one period to the next. By year, the score's correlation with the 28-day return swings from −0.46 to +0.48, and its correlation with the move is negative in 7 of 8 years (−0.06 to −0.31).
- F7: When the combined score disagreed in sign with the 28-day return (696 cases, 77 % of them short), its bets earned −1.26 % per case. When they agreed (576 cases), they earned +0.55 %.
