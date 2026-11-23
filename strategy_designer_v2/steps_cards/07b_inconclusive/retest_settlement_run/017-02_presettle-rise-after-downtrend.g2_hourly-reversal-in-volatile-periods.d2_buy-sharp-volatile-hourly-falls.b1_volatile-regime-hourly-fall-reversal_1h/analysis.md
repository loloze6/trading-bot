---
line: 7.b inconclusive
backtest: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d2_buy-sharp-volatile-hourly-falls.b1_volatile-regime-hourly-fall-reversal_1h
idea tested: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d2_buy-sharp-volatile-hourly-falls.b1_volatile-regime-hourly-fall-reversal
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3537 USD
---
## Findings
- **F1:** The main measure is on the predicted side but short of the bar: +0.089 % mean 24-hour excess per case, t 1.58 over 9,530 cases. At other horizons the same cases are clearer: +0.093 % at 6 hours (t 3.16), +0.117 % at 12 hours (t 2.84) and +0.240 % at 48 hours (t 3.16). The 24-hour reading is the weakest of the four.
- **F2:** The supporting check could not pass for a mechanical reason. The median forecast is the cap of 20 (more than half the cases sit at 20), so the "strictly above median" half is empty and the check returns None. Yet the effect is graded with the forecast: mean excess by forecast quartile is −0.007 %, +0.042 %, +0.122 % and +0.199 % (t −0.07 to 1.50).
- **F3:** The effect is graded by how far 24-hour volatility is raised against its 30-day average, and the plan's on/off line at a ratio of 1.0 admits mostly cases without it. Among the strategy's cases, the lower three ratio quartiles give −0.104 %, −0.079 % and +0.071 % (t −1.01 to 0.66), and the top quartile gives +0.506 % (t 3.49).
- **F4:** On all sharp falling hours (at least 1.5 usual moves, one per 24-hour cell), the 24-hour excess rises steadily with the volatility ratio. Below 1.0 it is −0.253 % (t −3.60, strength −0.081, n 4,523); from 1.0 to 1.3, +0.010 % (t 0.09); from 1.3 to 1.6, +0.351 % (t 2.13); from 1.6 to 2.0, +0.315 % (t 1.41); from 2.0 to 2.5, +1.179 % (t 2.73, strength 0.097); above 2.5, +1.539 % (t 2.84, n 337).
- **F5:** The effect is mixed across coins and years, which drowns the pooled t. By coin, XRP (+0.224 %, t 1.39) and ZEC (+0.311 %, t 1.81) carry it, while BTC, ETH, LTC and XMR sit near 0 (t −0.21 to 0.25). By year, 2018, 2019 and 2022 are negative (−0.24 % each, t down to −1.69) and 2024 is strongly positive (+0.453 %, t 3.57). Among high-volatility falls (ratio 1.3 or more), all six coins are positive (+0.15 % to +1.32 %).
- **F6:** The average case is too small to pay for a trade, but the high-volatility cases are not. The average unusual move is +0.09 % per case (strength 0.015), half of the 0.19 % cost of a trade. Falls at volatility ratios above 2.0 carry +1.2 % to +1.5 % per case, about six to eight times that cost.

## Ideas
- `017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d2_buy-sharp-volatile-hourly-falls.b1_volatile-regime-hourly-fall-reversal.b1_volatile-hourly-falls-more-coins` (from F1, F2, F5): Over the next 24 hours, a coin rises after a sharp falling hour, only while its 24-hour volatility is raised against its 30-day average. The larger that fall relative to the coin's usual hourly volatility, the larger the rise.
- `017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d2_buy-sharp-volatile-hourly-falls.b1_volatile-regime-hourly-fall-reversal.b2_fall-reversal-graded-by-volatility` (from F3, F4, F6): Over the next 24 hours, a coin rises after a sharp falling hour, and the rise is larger the further the coin's 24-hour volatility is raised above its 30-day average at that hour.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
