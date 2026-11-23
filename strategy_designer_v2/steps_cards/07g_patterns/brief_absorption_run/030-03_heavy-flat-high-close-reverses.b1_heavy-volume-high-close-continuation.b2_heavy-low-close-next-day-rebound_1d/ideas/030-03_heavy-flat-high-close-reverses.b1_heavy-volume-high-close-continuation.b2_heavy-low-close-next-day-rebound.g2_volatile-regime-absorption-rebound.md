---
brief: 030_absorption-day-close-location
source-idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b2_heavy-low-close-next-day-rebound
line: 7.g patterns
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b2_heavy-low-close-next-day-rebound_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's 20-day volatility is high, a heavy-volume day closing near its low is followed by a larger rise over the next 1 day. The nearer the close sits to the low, the larger that rise.
Consequence: Take the heavy-volume low-close rebound in volatile stretches and refuse it in calm ones.
Why:
- F2: On heavy-volume days the close-location effect sits in the coin's most volatile third. Split by 20-day volatility tercile, the slope is 6.49 % at t 4.77 in the high tercile (n 433), against 1.05 % at t 1.11 in the middle (n 427) and -0.50 % at t -0.72 in the low (n 432).
- F6: The tested effect is uneven over time and coins, which fits the book's failed Calmar.
