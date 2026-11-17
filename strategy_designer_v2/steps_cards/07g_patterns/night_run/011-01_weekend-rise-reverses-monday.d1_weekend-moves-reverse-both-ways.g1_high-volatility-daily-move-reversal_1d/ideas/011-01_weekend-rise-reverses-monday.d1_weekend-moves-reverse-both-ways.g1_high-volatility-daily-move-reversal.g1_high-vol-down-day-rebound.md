---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.d1_weekend-moves-reverse-both-ways.g1_high-volatility-daily-move-reversal
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.d1_weekend-moves-reverse-both-ways.g1_high-volatility-daily-move-reversal_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's 20-day volatility is high relative to its own 60-day average, a down day is followed by a rise over the next 1 day, and the larger that day's fall measured in its 20-day volatility, the larger the rebound.
Consequence: In elevated volatility, buy after falls in proportion to their vol-scaled size, rather than also shorting after rises, which carry no reversal.
Why:
- F1: The next-day reversal depends on how high volatility is. Volatility here is the coin's 20-day volatility over its 60-day average. In the top third, the next day's excess return against the vol-scaled move has slope -0.063 (t -3.89, n 3682), and the signed reversal return averages +0.45% (t 5.19). In the bottom third, the slope is +0.048 (t 1.85) and the reversal return is -0.04% (t -0.47).
- F2: In that high-volatility third, nearly all the reversal follows down days. Down days have slope -0.088 (t -2.48, n 1758), while up days have +0.010 (t 0.34, n 1924). The lowest vol-scaled-return quintile is followed by a +1.02% next-day excess return (t 4.96, n 737), while the top quintile gives only -0.19% (t -0.89). So the idea's sign-only down-versus-up check misses a graded rebound after falls.
