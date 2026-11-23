---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d2_buy-sharp-volatile-hourly-falls.b1_volatile-regime-hourly-fall-reversal
line: 7.b inconclusive
backtest: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d2_buy-sharp-volatile-hourly-falls.b1_volatile-regime-hourly-fall-reversal_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1h
period: folds A, B, C, D
---
Idea: Over the next 24 hours, a coin rises after a sharp falling hour, only while its 24-hour volatility is raised against its 30-day average. The larger that fall relative to the coin's usual hourly volatility, the larger the rise.
Consequence: A trader would buy sharp single-hour falls only when the coin's volatility is running above its monthly norm, scaled to the size of the fall, and would refuse to buy falls in calm or ordinary volatility.
Why:
- F1: The main measure is on the predicted side but short of the bar: +0.089 % mean 24-hour excess per case, t 1.58 over 9,530 cases. At other horizons the same cases are clearer: +0.093 % at 6 hours (t 3.16), +0.117 % at 12 hours (t 2.84) and +0.240 % at 48 hours (t 3.16). The 24-hour reading is the weakest of the four.
- F2: The supporting check could not pass for a mechanical reason. The median forecast is the cap of 20 (more than half the cases sit at 20), so the "strictly above median" half is empty and the check returns None. Yet the effect is graded with the forecast: mean excess by forecast quartile is −0.007 %, +0.042 %, +0.122 % and +0.199 % (t −0.07 to 1.50).
- F5: The effect is mixed across coins and years, which drowns the pooled t. By coin, XRP (+0.224 %, t 1.39) and ZEC (+0.311 %, t 1.81) carry it, while BTC, ETH, LTC and XMR sit near 0 (t −0.21 to 0.25). By year, 2018, 2019 and 2022 are negative (−0.24 % each, t down to −1.69) and 2024 is strongly positive (+0.453 %, t 3.57). Among high-volatility falls (ratio 1.3 or more), all six coins are positive (+0.15 % to +1.32 %).
