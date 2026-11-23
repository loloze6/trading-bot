---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d2_buy-sharp-volatile-hourly-falls.b2_extreme-hourly-fall-reversal
line: 7.g patterns
backtest: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d2_buy-sharp-volatile-hourly-falls.b2_extreme-hourly-fall-reversal_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: Over the next 24 hours, a coin rises after a fall over its past 24 hours, and the larger that 24-hour fall relative to the coin's hourly volatility over the past 7 days, the larger the rise.
Consequence: A trader would buy a coin after its largest volatility-scaled day-long falls and hold it for about a day, because the rise that follows is several times the cost of a trade.
Why:
- F1: A coin's 24-hour fall, measured against its own past week of hourly volatility, is followed by a graded rise over the next 24 hours. On non-overlapping 24-hour cells, the lowest decile shows a strength of +0.135 (t 4.5, 1626 cases), an unusual move of +0.71 % and a total move of +0.83 %. That total move is about 4.4 times the 0.19 % cost of a trade. The second decile shows +0.035 (t 1.4, 1625 cases), and deciles 3 to 10 sit between −0.04 and 0.
- F2: The reversal of the 24-hour move grows with its size. Signed against the move, the strength by quintile of its absolute size runs −0.012, −0.013, +0.024, +0.030 and +0.091, the last with t 4.7 over 3249 cases.
- F5: The 24-hour reversal holds across coins and years. The rank correlation between the 24-hour move in volatility units and the next 24-hour strength is negative in all 6 coins (−0.045 to −0.104) and in all 8 years (−0.029 to −0.116). The bottom-two-decile strength is positive in 7 of 8 years, the exception being 2022 at −0.012.
- F6: The same lowest-decile rise appears at other horizons. It is +0.129 at 12 hours (t 3.9) and +0.088 at 48 hours (t 3.3). Most of the move therefore shows within half a day and none of it is lost by 48 hours.
- F4: The single-hour fall the idea used is not graded at its extreme. Hours whose volatility-scaled return lies between −3 and −2 are followed by a 24-hour strength of +0.112 (t 2.2, 432 cases). Hours at or below −3 are followed by −0.112 (t −1.2, 154 cases). This explains why the tested idea's upper-minus-lower check failed (−0.055 %) and its strength was only 0.003.
