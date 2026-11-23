---
brief: 030_absorption-day-close-location
source-idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.g2_low-close-rebound-in-volatility
line: 7.g patterns
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.g2_low-close-rebound-in-volatility_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The heavier a coin's volume over the past day relative to its average daily volume over the past 20 days, on a day it closed higher, the more it rises over the next day.
Consequence: A trader buys after up days on unusually heavy volume, larger the heavier the volume, and refuses to buy after up days on ordinary volume.
Why:
- F4: Days of heavy volume relative to the coin's 20-day average are followed by a rise. In the top quarter of relative volume the next-day excess return is +0.329 % (t 3.57, n 4031), against −0.10 % to −0.12 % in the other three quarters. Log relative volume has t 5.07 controlling for the day's return and the location term, and t 2.59 on 5147 non-overlapping 3-day cases. The top quintile beats the rest in 71 % of the 24 windows.
- F5: The heavy-volume rise sits on up days, and its link is weaker per coin and per year. Top-quintile relative volume on up days is followed by +0.772 % (t 5.11, n 1546), while on down days it is followed by −0.031 % (t −0.22). Per coin the relative-volume slope reaches t ≥ 2 only in ZEC (3.24) and XRP (2.42), with t 0.55 to 1.74 elsewhere. By year it ranges from t 0.10 (2022) to 3.57 (2021).
