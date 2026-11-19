---
brief: 016_grind-versus-jump-moves
source-idea: 016-07_up-volume-burst-reversal.g1_efficient-rises-keep-rising
line: 7.g patterns
backtest: 016-07_up-volume-burst-reversal.g1_efficient-rises-keep-rising_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's past 24-hour return relative to its own usual hourly volatility over the past 30 days, the more the coin moves in the opposite direction over the next 24 hours.
Consequence: A coin that has just rallied hard for a day relative to its usual volatility is a reason to lighten or fade it for the next day, and one that has just dropped hard is a reason to buy it for the next day.
Why:
- F1: Over the next 24 hours, a coin gives back part of its past day's move. Regressing the next 24-hour excess return on the past 24-hour return, scaled by 30-day hourly volatility, gives a slope t of -5.59 (n=12926, non-overlapping 24h grid). The past 6-hour version gives t -4.82 and the past 12-hour version t -4.69. After a past-6h z of -2 or less, the next 24h excess is +0.74% (t 2.00, n=339); after a z of +2 or more it is -0.71% (t -2.08, n=313).
- F2: The 24-hour reversal is broad across coins and years. The slope is negative in all six coins (t from -0.51 for LTC to -3.30 for XMR) and in 7 of 8 years (2018 t -4.46, 2019 t -2.66, 2020 t -2.87; 2024 is the exception at t +1.64). In every coin, the next-24h excess after a 6h fall is above the excess after a 6h rise (BTC +0.13% vs -0.12%, ETH +0.29% vs -0.26%).
