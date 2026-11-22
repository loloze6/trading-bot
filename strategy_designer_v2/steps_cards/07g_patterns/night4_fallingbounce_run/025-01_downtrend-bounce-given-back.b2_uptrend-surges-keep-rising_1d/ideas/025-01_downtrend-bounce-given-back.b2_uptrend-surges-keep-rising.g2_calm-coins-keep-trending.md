---
brief: 025_bounces-fade-in-falling-markets
source-idea: 025-01_downtrend-bounce-given-back.b2_uptrend-surges-keep-rising
line: 7.g patterns
backtest: 025-01_downtrend-bounce-given-back.b2_uptrend-surges-keep-rising_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 20-day standard deviation of daily returns is low against its own past, the direction of its 90-day return continues over the next 5 days. The calmer the coin, the larger the move in that direction.
Consequence: In a calm coin, the sign of its 90-day return is a reason to hold a position its way for the next days, and in a turbulent coin it is no reason at all.
Why:
- F3: The coin's 90-day direction persists over 5 days only when the coin is calm. In the lowest third of each coin's 20-day volatility, a non-negative 90-day return is followed by +0.90 % excess over 5 days (t 2.39, 505 cases), and a negative one by -0.76 % (t -2.03, 491 cases). In the middle and top thirds, every mean is between -0.47 % and -0.05 % with |t| ≤ 0.93.
- F4: The book earns only when it holds large positions, which under vol targeting means calm coins. Held bars in the top quartile of allocation have a next-day excess return of +0.226 % (t 2.40, 2214 bars). The two lowest quartiles have -0.197 % (t -1.74) and -0.173 % (t -1.64).
