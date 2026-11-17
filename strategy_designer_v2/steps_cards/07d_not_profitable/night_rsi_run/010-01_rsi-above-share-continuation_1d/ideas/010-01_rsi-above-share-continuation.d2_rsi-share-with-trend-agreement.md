---
brief: 010_rsi-midline-regime-direction
source-idea: 010-01_rsi-above-share-continuation
line: 7.d not profitable
backtest: 010-01_rsi-above-share-continuation_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: The larger the share of the past 30 days that a coin's 14-day RSI has spent above its midpoint of 50, the higher the coin's return over the next 14 days, only while the coin's 90-day return has the same sign as that share's distance from one half.
Consequence: A trader should follow RSI's side only when the coin's 90-day trend points the same way, and should stand aside when the two disagree.
Why:
- F1: The book's chained daily returns fall at most -53.0% against a yearly return of 30.6% (Calmar 0.577, below the 0.75 needed), and the deepest fall runs 413 days across w2-w5, where short positions lose a summed -0.554 against -0.132 for long positions.
- F5: Both sides do better when the coin's own 90-day return agrees with them, though the 90-day sample covers only each window's late days: shorts average +0.00082 per day when the 90-day return is negative (n=563) and -0.00036 when it is positive (n=164); longs average +0.00269 when it is positive (n=626) and -0.00258 when it is negative (n=150); longs in the top 90-day-return fifth average +0.0059 (n=294) against -0.00596 in the bottom fifth (n=29).
