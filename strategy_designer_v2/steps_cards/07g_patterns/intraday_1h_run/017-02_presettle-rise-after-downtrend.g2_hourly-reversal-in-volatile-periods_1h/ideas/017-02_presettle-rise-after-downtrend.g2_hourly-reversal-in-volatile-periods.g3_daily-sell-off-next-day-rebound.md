---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods
line: 7.g patterns
backtest: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: Over the next 24 hours, a coin rises after a fall over its last 24 hours. The deeper that fall relative to its usual hourly volatility, the larger the rise.
Consequence: A trader would buy coins after a day-long sell-off scaled by volatility, holding for a day, and would refuse such trades if the rebound is not confirmed.
Why:
- F5: Larger multi-hour moves also revert over the next 24h on non-overlapping grids. After the bottom fifth of volatility-scaled 4h moves, the 24h excess return is +0.003466 (t 3.9, n 3,424), against -0.002018 (t -2.3) in the fourth fifth. After the bottom fifth of scaled 24h moves it is +0.003511 (t 3.8), with the upper fifths near -0.0016 (t about -1.9).
- F4: The reversal of the scaled one-hour move lasts well beyond one hour on non-overlapping grids. After the bottom fifth of scaled moves, the excess return is +0.000749 (t 4.8, n 20,646) over 4h and +0.002362 (t 2.8, n 3,422) over 24h. After the top fifth it is -0.000494 (t -3.5) over 4h and -0.003228 (t -3.8, n 3,425) over 24h.
