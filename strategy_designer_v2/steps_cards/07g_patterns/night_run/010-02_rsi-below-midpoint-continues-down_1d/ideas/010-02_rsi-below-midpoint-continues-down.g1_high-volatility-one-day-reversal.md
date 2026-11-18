---
brief: 010_rsi-midline-regime-direction
source-idea: 010-02_rsi-below-midpoint-continues-down
line: 7.g patterns
backtest: 010-02_rsi-below-midpoint-continues-down_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 20-day volatility is high, the larger its 1-day return relative to that volatility, the larger the move the opposite way over the next 1 day, and the higher the volatility, the stronger this reversal.
Consequence: After an outsized daily move in a volatile market, a trader would lean against it for the next day rather than follow it, and would decline to chase it.
Why:
- F1: The next-day excess return runs against today's volatility-scaled return mainly when volatility is high: in the top tercile of 20-day volatility the slope is -0.0062 (t -4.91, n 1612), while the middle tercile shows no effect (t -0.73, n 1610) and the low tercile leans the other way (t +2.07, n 1612).
- F2: Pooled over BTC and ETH, today's return points the opposite way to tomorrow's excess return, with slope -0.086 on the raw return (t -6.08, n 4834) and t -2.92 on the volatility-scaled return. This holds in both coins (BTC t -1.62, ETH t -2.44) and has a negative slope in 6 of 8 years (2020 t -2.98).
- F3: The reversal does not last past a day: on 3-day non-overlapping samples, the slope of the 3-day excess return on today's scaled return is t -0.13 (n 1571).
