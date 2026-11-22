---
brief: 023_range-reversion-when-no-trend
source-idea: 023-01_flat-range-top-reverts-down.d1_flat-top-reverts-after-rise.b1_range-top-continues-in-risers
line: 7.g patterns
backtest: 023-01_flat-range-top-reverts-down.d1_flat-top-reverts-after-rise.b1_range-top-continues-in-risers_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 90-day return is positive, the larger its last day's return measured in units of its daily volatility, the more it rises over the next 5 days.
Consequence: A trader would buy into, not fade, a strong up-day in a coin rising over the past 90 days.
Why:
- F4: Inside the trending regime, recent strength of any length precedes more rise over the next 5 days. Slopes of the demeaned 5-day return: 1-day return in volatility units 0.0094 (t 3.15), 5-day 0.0087 (t 2.86), 20-day 0.0096 (t 3.33), over 1549 / 1549 / 1465 cases. The same slopes in the unknown regime have |t| ≤ 1.33.
- F5: In the trending regime, the 5-day move is lopsided across range quintiles. The top range quintile is followed by +1.14 % demeaned (t 1.99, 495 cases) and the second-lowest by −1.44 % (t −2.39, 186 cases). The unknown regime shows no quintile with |t| > 0.6.
