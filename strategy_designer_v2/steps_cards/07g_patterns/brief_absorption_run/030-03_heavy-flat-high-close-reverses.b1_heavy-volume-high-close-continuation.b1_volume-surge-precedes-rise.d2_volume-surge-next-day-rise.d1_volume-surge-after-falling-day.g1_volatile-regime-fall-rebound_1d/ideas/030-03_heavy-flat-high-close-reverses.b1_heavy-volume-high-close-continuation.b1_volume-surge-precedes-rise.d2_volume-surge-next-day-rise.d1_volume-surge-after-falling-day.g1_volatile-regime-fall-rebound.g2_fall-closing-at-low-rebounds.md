---
brief: 030_absorption-day-close-location
source-idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day.g1_volatile-regime-fall-rebound
line: 7.g patterns
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day.g1_volatile-regime-fall-rebound_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The more a coin's one-day fall ends with its close near the day's low rather than recovered toward the high, the more the coin rises over the next day. The rebound after a fall grows with how near the low the day closed, more than with how deep the fall was.
Consequence: A trader buying sharp daily falls favours those that closed at the day's low and refuses falls that already recovered toward the high within the day.
Why:
- F1: On falling days, a pooled regression of the next-day excess return gives the close's distance from the day's high (low close) times log volume against its 20-day mean a coefficient of +0.0181 (t 4.10, n 7151), and low close alone +0.0099 (t 2.92). The fall's own depth in usual moves adds nothing once these are in (+0.0001, t 0.11). So the tested idea's rebound is carried by closes near the low on heavy volume, not by how deep the fall was.
- F5: Inside the tested idea's positive forecasts, the close location splits the result:
