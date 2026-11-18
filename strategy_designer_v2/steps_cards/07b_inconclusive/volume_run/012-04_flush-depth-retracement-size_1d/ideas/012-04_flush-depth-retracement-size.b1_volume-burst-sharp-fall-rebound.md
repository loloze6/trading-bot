---
brief: 012_liquidation-flush-partial-rebound
source-idea: 012-04_flush-depth-retracement-size
line: 7.b inconclusive
backtest: 012-04_flush-depth-retracement-size_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: Among bars that fall sharply, the larger the bar's volume relative to its mean over the prior 20 days, the larger the price rise over the next 3 days.
Consequence: After a sharp daily fall, the heavier the volume burst, the stronger the case for buying the rebound over the following few days rather than selling into it.
Why:
- F5: Among all sharp falls, the volume ratio to its prior 20-day mean predicts the rebound in grade. Its slope is t 3.99 over 1 day, 3.24 over 2 days and 2.53 over 3 days (n 351–354), and it fades by 5 days (t −0.52).
- F4: The long-lower-wick condition works against the rebound. Among all 354 declustered sharp falls, the wick-over-range slope on the excess return is t −3.34 at 1 day and −1.96 at 3 days. The highest wick quartile averages −0.0112 over 3 days and the lowest +0.0131. Volume-burst falls without the wick average +0.0100 (n 119); those with it average −0.0026 (n 41).
- F2: The flush bars show no rebound distinct from other sharp falls. Their mean excess 3-day return is +0.0022 (t 0.28, n 75), against +0.0012 for the 351 other sharp falls (Welch t 0.11). At 1 day the flush bars do worse: −0.0099 against +0.0092 (Welch t −2.53).
