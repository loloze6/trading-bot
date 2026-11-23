---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d1_day-long-fade-of-sharp-hours
line: 7.g patterns
backtest: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d1_day-long-fade-of-sharp-hours_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: In the two hours from 15:00 to 17:00 UTC, around the 16:00 funding settlement, a coin continues the direction of its 24-hour return. The larger that 24-hour return relative to the coin's hourly volatility over the past 24 hours, the larger the move over those two hours.
Consequence: A trader would time entries in the direction of a strong 24-hour move into the hours around the 16:00 UTC settlement rather than fade it there.
Why:
- F3: The hours 15:00 to 17:00 UTC, which straddle the 16:00 settlement, also continue the 24-hour move, graded by its size. The with-trend return runs −1.79 bp in the smallest |z24| quintile and +7.13 bp (t 4.71) in the fourth. It is +9.61 bp in the largest (t 5.18, n 6,573). By year it is unstable: +14.9 bp (t 8.0) in 2020, −5.1 bp (t −3.4) in 2022.
- F4: Outside 15:00, 16:00 and 21:00 to 23:00, the largest 24-hour moves partly reverse the next hour: −3.54 bp (t −6.91, n 65,825) in the top |z24| quintile, against −0.18 bp in the bottom quintile. Pooled over all those other hours, the against-trend return is only +0.99 bp (t 5.27).
