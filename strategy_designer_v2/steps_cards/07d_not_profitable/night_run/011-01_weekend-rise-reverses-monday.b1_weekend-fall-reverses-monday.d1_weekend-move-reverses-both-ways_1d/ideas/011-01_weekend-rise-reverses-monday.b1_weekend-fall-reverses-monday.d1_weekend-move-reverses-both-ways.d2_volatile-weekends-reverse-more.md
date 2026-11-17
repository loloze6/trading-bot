---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.d1_weekend-move-reverses-both-ways
line: 7.d not profitable
backtest: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.d1_weekend-move-reverses-both-ways_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's return over the next 3 days runs against its Sunday close-to-close move. The size of that move back, in price terms, grows with the coin's 20-day volatility of daily returns, so the same weekend move scaled to usual size is undone more when the coin has been volatile.
Consequence: A trader would size the weekend fade by recent volatility and take larger positions in volatile spells, instead of the largest positions on the most extreme weekend moves.
Why:
- F5: The reversal rises with the coin's 20-day volatility, measured as the 1-day reversal net of each coin's mean. It is 0.0007, 0.0057 and 0.0114 from the lowest to the highest volatility tercile (3-day: 0.0033, 0.0086, 0.0151). The low-volatility tercile has a negative book gain (−0.0007).
- F3: Sizing is inverted at the extremes. The largest-rise quintile carries the biggest positions (mean |position| 0.81, mean |forecast| 14.9) but reverses least over 1 day (0.0017) and loses money (mean gain −0.0021). In the top quartile of |z| the 1-day reversal is about 0 in both trend states (−0.0009 and −0.0008), while the middle quartiles reverse most (0.015–0.018 in down-trends).
- F2: The move back does not end after one day; it keeps building through day 3. On the 1,817 Sunday cases, the reversal net of each coin's mean is 0.0059 (1 day) vs 0.0123 (3 days) in the largest-fall quintile, 0.0093 vs 0.0123 in the fourth quintile, and 0.0017 vs 0.0094 in the largest-rise quintile. The one-bar hold keeps less than half of it.
