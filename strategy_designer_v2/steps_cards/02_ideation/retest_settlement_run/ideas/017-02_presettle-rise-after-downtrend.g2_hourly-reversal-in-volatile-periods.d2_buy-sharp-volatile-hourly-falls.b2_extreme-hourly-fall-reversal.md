---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d2_buy-sharp-volatile-hourly-falls
line: 7.b inconclusive
backtest: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d2_buy-sharp-volatile-hourly-falls_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: Over the next 24 hours, a coin rises after a sharp falling hour, and the larger that fall relative to the coin's usual hourly volatility, the larger the rise, while ordinary falls are followed by no rise.
Consequence: A trader would buy only the most extreme single-hour falls, measured in the coin's own hourly volatility, and hold them for a day.
Why:
- F4: The test measured the idea away from where it shows. Its cases are any rise of the forecast of 2 points, which are mostly ordinary falls. Across all regimes, the largest fifth of scaled falls gives +0.57 % excess over 24 hours (t 4.07), while the middle fifths give +0.09 %, +0.06 % and -0.17 % (t 0.79, 0.47, -1.59).
- F2: Inside the high-volatility third, the reversal is graded by the size of the fall. Mean 24-hour excess by fifth of the scaled fall, largest to smallest: +1.26 % (t 4.21), +0.86 % (t 3.21), +0.53 % (t 2.39), +0.20 % (t 0.80), -0.07 % (t -0.33), about 550 cases each.
