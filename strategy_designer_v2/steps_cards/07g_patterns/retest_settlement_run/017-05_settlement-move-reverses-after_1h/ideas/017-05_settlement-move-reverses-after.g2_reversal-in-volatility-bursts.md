---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after
line: 7.g patterns
backtest: 017-05_settlement-move-reverses-after_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's volatility over the past day is high against its volatility over the past 30 days, its 24-hour return is given back over the next 24 hours, more so the larger that return is.
Consequence: A trader fades large one-day moves mainly when the coin's recent volatility has jumped above its monthly norm.
Why:
- F4: The one-day reversal grows with the volatility regime. Among large moves, it is +0.043 % (t 0.4) in the lowest quartile of last-day volatility over 30-day volatility and +0.938 % (t 5.5) in the highest. By tercile of 30-day volatility, it is −0.079 % (t −0.7) in the lowest and +1.531 % (t 6.0, 969 cases) in the highest.
- F3: The one-day reversal is graded and concentrated in the largest moves. By quintile of the 24-hour move scaled by 30-day volatility, the contrarian return rises from −0.118 % (t −1.4) through +0.017 %, +0.287 % (t 3.2) and +0.508 % (t 4.8). Regressing the next-day return on the past-day return gives a negative slope in all 6 coins (−0.068 to −0.126, p ≤ 0.0004).
