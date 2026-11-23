---
brief: 030_absorption-day-close-location
source-idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.g2_low-close-rebound-in-volatility
line: 7.d confirmed, not profitable
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.g2_low-close-rebound-in-volatility_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The higher a coin's 20-day daily volatility, the more a day that closed near its low is followed by a rise over the next day. The rise appears only when the close sits in the lower part of the day's range and the volatility is high together, and it grows with how low the close sits and how high the volatility is.
Consequence: A trader takes the next-day long only when a low close meets a volatile stretch, sized up the deeper the close and the higher the volatility, and is out otherwise, which keeps the book clear of the coin's long falls.
Why:
- F5: The idea's own joint situation (top-half 20-day volatility and a lower-half close) gives a deepest fall of only −20 %, Calmar 1.01, Sharpe 0.96 and yearly +20.1 %, while in a position 19 % of the time, and it gained +20.9 % through w12–w14.
- F6: Neither condition earns alone, so the joint situation is the idea itself and not a separate effect.
- F7: The strong case holds in both 20-day trend states, so a trend filter is not the repair. High-volatility low closes are followed by +0.42 % (t 3.16, n 1865) after a falling 20 days and +0.62 % (t 4.60, n 1501) after a rising 20 days. Adding a rising-trend filter to forecast ≥ 15 lowers Calmar to 0.48.
- F3: Inside the deepest fall (w12–w14), the weak forecasts are what lose. Quintiles 1 and 2 lose −0.113 % and −0.236 % per bar on next-day moves of −0.56 % and −0.55 %, while the top quintile still gains +0.250 % (next-day move +0.53 %).
