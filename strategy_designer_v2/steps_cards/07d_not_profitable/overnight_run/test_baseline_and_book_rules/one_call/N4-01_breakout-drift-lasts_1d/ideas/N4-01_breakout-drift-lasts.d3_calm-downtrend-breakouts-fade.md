---
brief: 002_moving-average-cross-trend-persistence
source-idea: N4-01_breakout-drift-lasts
line: 7.d not profitable
backtest: N4-01_breakout-drift-lasts_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A new 20-day closing high reached in a calm coin (low 20-day volatility) that is in a 50-day downtrend is followed by a fall back below the high over the next days.
Consequence: Refuse breakout longs in calm downtrending coins, the one state where the book's contribution was negative.
Why:
- F8: Calm downtrends are the one losing state in the book's contribution. Coin-days in a 50-day downtrend with the lowest-tercile 20-day volatility contributed -0.376, while uptrend coin-days contributed +1.18, +1.07 and +0.71 across the three volatility terciles.
- F2: On the book's worst 5% of days it lost -10.0% while the coins' average lost -7.3%. On those days 89% of coins were held, against 59% on an average day, and only 36% of coins were in a 50-day uptrend. The big falls come from being fully long into a market-wide drop.
- F4: Gains come from coins in a 50-day uptrend. When a coin was 50-day uptrending, its held days earned 0.00419 a day (t 3.86, n 4,258 coin-days). When it was 50-day downtrending, held days earned 0.00144 (t 0.82, n 1,935). Yet the book was still exposed 38% of the time in downtrends.
