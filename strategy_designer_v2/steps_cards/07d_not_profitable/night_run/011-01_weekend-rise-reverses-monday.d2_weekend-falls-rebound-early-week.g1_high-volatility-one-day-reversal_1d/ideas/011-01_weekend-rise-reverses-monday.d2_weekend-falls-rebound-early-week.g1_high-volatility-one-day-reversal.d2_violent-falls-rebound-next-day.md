---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.d2_weekend-falls-rebound-early-week.g1_high-volatility-one-day-reversal
line: 7.d not profitable
backtest: 011-01_weekend-rise-reverses-monday.d2_weekend-falls-rebound-early-week.g1_high-volatility-one-day-reversal_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin whose last day's move was large relative to its 20-day volatility moves the opposite way over the next 1 day, and the reversal is larger the larger that scaled move and the higher the coin's 20-day volatility stands against its own history, except after an up day, when the coin keeps the drift it had over its last 20 days.
Consequence: Buy the bounce after violent down days in turbulent markets, but do not short violent up days, especially in a rising market.
Why:
- F4: The short side carries the losses. Short bars earn 0.000261 timing per bar against 0.001481 for long bars (about 8.4k to 8.9k bars each). In the high-volatility tercile shorts net -0.000226 per bar while longs net 0.004040 (t 4.52, n 1408).
- F5: Shorting an up day while the coin's 20-day return is up is the worst case: net -0.001477 per bar (t -2.95, n 4089). Buying a down day nets 0.001187 in a 20-day downtrend (t 2.52) and 0.001265 in an uptrend (t 2.88).
- F2: The fade loses after costs in every volatility state except the most turbulent. Split by the coin's 20-day volatility against its 120-bar mean absolute move, the four lowest sextiles net -0.000706 to -0.001039 per bar (t -1.15 to -1.87, about 1480 bars each), the fifth nets 0.000429 (t 0.43), and only the top sextile (ratio 2.25) nets 0.003212 (t 3.49).
