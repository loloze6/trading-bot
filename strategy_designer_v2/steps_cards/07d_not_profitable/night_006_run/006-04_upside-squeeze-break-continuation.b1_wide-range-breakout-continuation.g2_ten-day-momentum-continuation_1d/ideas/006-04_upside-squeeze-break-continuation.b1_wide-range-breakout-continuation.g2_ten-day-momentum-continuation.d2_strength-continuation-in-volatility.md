---
brief: 006_range-compression-precedes-expansion
source-idea: 006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation.g2_ten-day-momentum-continuation
line: 7.d not profitable
backtest: 006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation.g2_ten-day-momentum-continuation_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The higher a coin's 10-day return, and the closer its close sits to the top of its prior 20-day range, the further its price rises over the next 10 days, and the higher its 20-day volatility, the larger that rise.
Consequence: A trader would keep, or enlarge, longs on strong coins in volatile stretches rather than cutting them by volatility, and would not short in those stretches.
Why:
- F2: On the non-overlapping 10-day grid the forecast's information sits only at its top. The top quintile's excess 10-day return was +0.0247 (t 2.50, n=338) and the middle quintile's was -0.0209 (t -2.51). The bottom quintile, which the book shorts hardest, was +0.0006 (t 0.07, n=339), so a weak 10-day return and a close far below the 20-day top did not come before below-average returns.
- F5: The book's mean daily return was about 0.000251 a bar against the coins' 0.0007 to 0.0016 a day from holding. Its mean absolute position was only 0.235 and it was short 47% of bars, so its Sharpe was 0.32 against 0.55 for holding, and its Calmar was 0.11.
- F6: In the high-volatility tercile, longs held a position of only 0.176 while the coin rose 0.003853 a day, earning 0.000547. Shorts there lost 0.000447 a bar while the coin rose 0.001759.
