---
brief: 016_grind-versus-jump-moves
source-idea: 016-05_up-even-volume-continuation.g1_evening-utc-hour-drift.d1_efficient-rise-keeps-rising
line: 7.d not profitable
backtest: 016-05_up-even-volume-continuation.g1_evening-utc-hour-drift.d1_efficient-rise-keeps-rising_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The more efficiently a coin has risen over its past 3 days (its 3-day rise large relative to the sum of its absolute hourly moves), the more it keeps rising over the next 3 days, only while its 30-day return is positive.
Consequence: An efficient 3-day rise is a reason to be long only inside a coin's 30-day uptrend; in a 30-day downtrend it is a reason to stay out, which removes the exposure that carries the deepest falls.
Why:
- F1: The Calmar failure comes from the book's falls riding the coins' own declines. The chained book returns 26.8 % a year, but its deepest fall is 48.1 %. Its five deepest falls (48 %, 44 %, 42 %, 35 %, 34 %) each last 157 to 611 days. In each, the coins' own chained return to the trough is -37 % to -81 % (-81 % in the deepest, troughing in w14).
- F2: The book is almost always long: 91 % of all bars. It is long on 98 % of "trending" bars and still on 83 % of "unknown" bars, where the 3-day return is not positive and the forecast is 0. The 72-bar minimum hold keeps it long there, so it carries most of each coin decline.
- F3: The book's hourly gain is concentrated in coins whose 30-day return is positive.
- F4: On the 72-bar grid, the idea's effect appears only with a positive 30-day return.
- F5: Across all positive-forecast cases, the efficiency effect is graded only at its top. Excess 72-bar returns by efficiency quintile run -0.51 %, -0.22 %, -0.10 %, +0.20 %, +1.16 % (top t 2.87, 573 cases each). The idea's overall unusual move is -0.13 % per case, so most of the forecast range sizes the book on noise.
