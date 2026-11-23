---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d2_buy-sharp-volatile-hourly-falls.b2_extreme-hourly-fall-reversal
line: 7.g patterns
backtest: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d2_buy-sharp-volatile-hourly-falls.b2_extreme-hourly-fall-reversal_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's hourly volatility over the past 7 days is high for that coin, its next 24 hours run against its past 24-hour move. The larger that move relative to the coin's volatility, and the higher that volatility, the larger the move back.
Consequence: A trader would fade large day-long moves in either direction only while the coin is in a turbulent week, and would refuse to fade them in calm weeks.
Why:
- F3: The reversal depends on volatility. Among the two largest quintiles of 24-hour moves, the reversal strength is +0.224 (t 7.1, 2094 cases) in the highest tercile of 7-day hourly volatility. It is +0.009 (t 0.5) in the middle tercile and −0.045 (t −3.0, 2155 cases) in the lowest tercile, where moves continue instead.
- F2: The reversal of the 24-hour move grows with its size. Signed against the move, the strength by quintile of its absolute size runs −0.012, −0.013, +0.024, +0.030 and +0.091, the last with t 4.7 over 3249 cases.
- F7: The book is almost always long, so it follows the market. It held a position on 99 % of coin-days. Its mean daily return is negative in the two falling years, −0.23 % a day in 2018 (t −3.0) and −0.225 % a day in 2022 (t −2.7). It beats holding the coin only on Sundays (+0.073 % a day, t 2.0).
