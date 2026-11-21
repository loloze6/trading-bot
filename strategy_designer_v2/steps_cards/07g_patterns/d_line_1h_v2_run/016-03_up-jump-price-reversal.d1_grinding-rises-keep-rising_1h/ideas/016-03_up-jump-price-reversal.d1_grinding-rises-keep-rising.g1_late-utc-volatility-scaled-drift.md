---
brief: 016_grind-versus-jump-moves
source-idea: 016-03_up-jump-price-reversal.d1_grinding-rises-keep-rising
line: 7.g patterns
backtest: 016-03_up-jump-price-reversal.d1_grinding-rises-keep-rising_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: In each coin, the price rises over the 21:00–23:00 UTC hours, and the rise is larger the higher the coin's average absolute hourly return over the past 3 days.
Consequence: A trader would hold a coin long through the 21:00–23:00 UTC hours each day, sizing up when its recent hourly swings are large, and would avoid shorting into that window.
Why:
- F1: Each coin's hourly returns in the 21:00 and 22:00 UTC bars are positive on their own: BTC +4.3bp (t 4.5), ETH +5.6bp (t 4.6), LTC +4.9bp (t 3.7), XMR +4.9bp (t 3.6), XRP +4.8bp (t 3.0) and ZEC +5.4bp (t 3.3), with about 5,600 to 5,800 non-overlapping hourly cases per coin; pooled, hour 21 gives +5.5bp (t 6.9) and hour 22 gives +4.4bp (t 5.8), against roughly 0 to 1bp in most other hours.
- F2: The 21:00–22:00 UTC rise grows with the coin's trailing 72-hour mean absolute hourly return: +2.1bp (t 3.2) in the lowest volatility quintile, then +2.0, +4.2, +4.7 and +11.4bp (t 5.5) in the highest, with about 6,800 hours per quintile.
- F3: The 21:00–22:00 UTC rise is positive in 7 of 8 years (2018 +5.1bp t 2.3, 2019 +5.9bp t 4.5, 2020 +8.6bp t 5.3, 2021 +9.8bp t 5.4, 2023 +2.0bp t 1.9, 2024 +6.9bp t 5.7, 2025 +3.6bp t 2.4; only 2022 is −2.2bp t −1.5) and on every weekday (+2.8 to +5.6bp); the other hours average −1.7 to +1.2bp in the same years.
