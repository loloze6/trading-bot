---
brief: 016_grind-versus-jump-moves
source-idea: 016-01_up-grind-price-continuation.g1_big-moves-precede-rises
line: 7.g patterns
backtest: 016-01_up-grind-price-continuation.g1_big-moves-precede-rises_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The straighter a coin's last 24 hours (its net 24-hour move over the sum of its absolute hourly moves), the more the coin rises over the next 24 hours.
Consequence: A trader leans long, and harder, after a day whose hourly path went steadily one way, and holds back after a choppy day.
Why:
- F4: The straightness of the last 24 hours, in either direction, is followed by a higher return over the next 24 hours: slope 0.0176, t=3.92, n=5,539. It is also followed by a higher return over the next 72 hours: slope 0.0231, t=3.06.
