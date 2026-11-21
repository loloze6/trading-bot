---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.d2_extreme-daily-run-reverses
line: 7.d not profitable
backtest: 017-05_settlement-move-reverses-after.d2_extreme-daily-run-reverses_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's 24-hour return relative to its usual 24-hour move, the larger its move in the opposite direction over the next 24 hours, with the reversal concentrated in the most extreme moves. This holds only when that return is a fall, and only while the coin's past-week hourly volatility is high against its past-month volatility; the higher that ratio, the larger the rebound.
Consequence: A trader buys a coin's deepest daily falls when its volatility has just jumped, expecting a rebound many times the cost, and refuses to short its daily rises.
Why:
- F1: The idea is far too small for this book to pay. Its move per case is +0.06 % over 24 hours (0.013 of a usual 4.87 % move, 16146 cases), which is 0.3 times the 0.19 % cost of a buy and a sell. The book trades 2.71 times a day, about 8000 trades per coin, with a median hold of 29 to 32 hours. Its mean net result per trade is -0.08 % to -0.48 % on every coin, so the daily mean is -0.066 % and the Sharpe -0.57, against holding's +0.55.
- F2: The book loses before costs, and it loses on the short side. Its gross gain per bar is +0.08 bps overall: -0.35 bps per bar on its 215874 short bars and +0.55 bps per bar on its 199974 long bars. The mean gross result per trade is negative on 5 of 6 coins (-0.14 % to -0.38 %).
- F3: The reversal exists only after falls. On non-overlapping 24-hour grid cases, drift-adjusted, the next 24 hours after the 10 % deepest 24-hour falls (in units of the coin's usual move) average +0.71 % (t 4.69, 1639 cases). After the 10 % largest rises they average -0.20 % (t -1.62), a continuation the book is short against. Over 72 hours those top-decile rises go on to +0.72 % (t 3.14).
- F4: The rebound after deep falls is concentrated where the past week's hourly volatility is high against the past month's. In the deepest fall decile with the top quarter of that ratio (mean 1.32), the next 24 hours give +2.53 % (t 5.74, 350 cases) and the next 72 hours +2.33 % (t 4.84). The other three volatility quarters give -0.09 % to +0.45 % (|t| ≤ 1.5).
- F5: Inside the high-volatility state the rebound is graded by the size of the fall. Over 24 hours, the fall quintiles from deepest to mildest give +2.43 % (t 5.65), +0.84 %, +0.80 %, +0.42 % and -0.32 %, about 360 cases each.
- F6: The high-volatility fall rebound holds in every quarter of the windows (+0.79 %, +1.41 %, +2.82 %, +1.30 % over 24 hours; t 1.8 to 4.1, 164 to 202 cases each). This is 4 to 15 times the 0.19 % cost, where the tested idea's whole move is 0.3 times it.
