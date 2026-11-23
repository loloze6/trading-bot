---
brief: 030_absorption-day-close-location
source-idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d1_extreme-surge-low-close-rise
line: 7.g patterns
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d1_extreme-surge-low-close-rise_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's one-day return relative to its own 20-day volatility, the more the coin moves the opposite way over the next three days. The reversal is stronger the higher the coin's 20-day volatility.
Consequence: In turbulent stretches, a trader buys after the sharpest volatility-scaled down days and sells after the sharpest up days, sized by how extreme the day was.
Why:
- F1: The next day reverses the day's return measured against its own 20-day volatility, and this grows with the coin's volatility. The slope of the next-day excess return on that scaled return goes from +0.0012 (t 2.1, 3197 cases) in the calmest fifth of 20-day volatility to −0.0090 (t −7.3, 3197 cases) in the most volatile fifth. In a regression on all days, the interaction with the high-volatility fifth is −0.0087 (t −3.4).
- F2: The high-volatility reversal holds in all six coins: slopes −0.0058 to −0.0159, with t from −1.6 (XRP, ZEC) to −5.5 (XMR), about 530 cases each. It also holds in every year from 2018 to 2024 (t −3.4, −1.0, −5.0, −4.1, −2.9, −3.1, −0.8). Only 2025 has the opposite sign (+0.0037, t 0.6, 208 cases).
- F3: The reversal outlasts the next day. In the high-volatility fifth, days in the lowest fifth of scaled return gain +1.16 % over 2 days (t 1.8, 302 cases) and +2.27 % over 3 days (t 2.3, 169 cases) beyond drift. Days in the highest fifth lose −1.03 % (t −2.1, 322 cases) and −1.41 % (t −1.8, 181 cases).
- F4: In the most volatile fifth, the tested idea's low-close effect vanishes once the day's scaled return is in the regression: the close-location slope is +0.00015 (t 0.08) against −0.0090 (t −3.7) for the scaled return. Within that regime, the edge from the low close is largely the reversal of a down day.
