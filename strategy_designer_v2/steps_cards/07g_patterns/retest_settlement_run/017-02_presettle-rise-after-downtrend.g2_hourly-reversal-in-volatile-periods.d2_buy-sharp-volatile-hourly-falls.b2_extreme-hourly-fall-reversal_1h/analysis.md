---
line: 7.g patterns
backtest: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d2_buy-sharp-volatile-hourly-falls.b2_extreme-hourly-fall-reversal_1h
idea tested: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d2_buy-sharp-volatile-hourly-falls.b2_extreme-hourly-fall-reversal
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3977 USD
---
## Findings
- **F1:** A coin's 24-hour fall, measured against its own past week of hourly volatility, is followed by a graded rise over the next 24 hours. On non-overlapping 24-hour cells, the lowest decile shows a strength of +0.135 (t 4.5, 1626 cases), an unusual move of +0.71 % and a total move of +0.83 %. That total move is about 4.4 times the 0.19 % cost of a trade. The second decile shows +0.035 (t 1.4, 1625 cases), and deciles 3 to 10 sit between −0.04 and 0.
- **F2:** The reversal of the 24-hour move grows with its size. Signed against the move, the strength by quintile of its absolute size runs −0.012, −0.013, +0.024, +0.030 and +0.091, the last with t 4.7 over 3249 cases.
- **F3:** The reversal depends on volatility. Among the two largest quintiles of 24-hour moves, the reversal strength is +0.224 (t 7.1, 2094 cases) in the highest tercile of 7-day hourly volatility. It is +0.009 (t 0.5) in the middle tercile and −0.045 (t −3.0, 2155 cases) in the lowest tercile, where moves continue instead.
- **F4:** The single-hour fall the idea used is not graded at its extreme. Hours whose volatility-scaled return lies between −3 and −2 are followed by a 24-hour strength of +0.112 (t 2.2, 432 cases). Hours at or below −3 are followed by −0.112 (t −1.2, 154 cases). This explains why the tested idea's upper-minus-lower check failed (−0.055 %) and its strength was only 0.003.
- **F5:** The 24-hour reversal holds across coins and years. The rank correlation between the 24-hour move in volatility units and the next 24-hour strength is negative in all 6 coins (−0.045 to −0.104) and in all 8 years (−0.029 to −0.116). The bottom-two-decile strength is positive in 7 of 8 years, the exception being 2022 at −0.012.
- **F6:** The same lowest-decile rise appears at other horizons. It is +0.129 at 12 hours (t 3.9) and +0.088 at 48 hours (t 3.3). Most of the move therefore shows within half a day and none of it is lost by 48 hours.
- **F7:** The book is almost always long, so it follows the market. It held a position on 99 % of coin-days. Its mean daily return is negative in the two falling years, −0.23 % a day in 2018 (t −3.0) and −0.225 % a day in 2022 (t −2.7). It beats holding the coin only on Sundays (+0.073 % a day, t 2.0).
- **F8:** There are strong hour-of-day effects, but they are too small to cover a trade. The bar after the 20 UTC and 21 UTC bars returns +0.044 and +0.062 of an hourly volatility (t 4.7 and 6.7, about 17 000 hours each), while the bar after 13 UTC returns −0.048 (t −4.1). Each is only a few hundredths of a percent, far under the 0.19 % cost.

## Ideas
- `017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d2_buy-sharp-volatile-hourly-falls.b2_extreme-hourly-fall-reversal.g1_day-long-fall-reversal` (from F1, F2, F5, F6, F4): Over the next 24 hours, a coin rises after a fall over its past 24 hours, and the larger that 24-hour fall relative to the coin's hourly volatility over the past 7 days, the larger the rise.
- `017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d2_buy-sharp-volatile-hourly-falls.b2_extreme-hourly-fall-reversal.g2_volatile-week-day-reversal` (from F3, F2, F7): When a coin's hourly volatility over the past 7 days is high for that coin, its next 24 hours run against its past 24-hour move. The larger that move relative to the coin's volatility, and the higher that volatility, the larger the move back.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
