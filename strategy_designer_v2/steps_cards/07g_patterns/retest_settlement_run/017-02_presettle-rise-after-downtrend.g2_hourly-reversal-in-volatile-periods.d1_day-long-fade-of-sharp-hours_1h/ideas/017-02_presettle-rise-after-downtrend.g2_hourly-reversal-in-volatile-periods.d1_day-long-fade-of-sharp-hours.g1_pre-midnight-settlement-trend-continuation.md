---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d1_day-long-fade-of-sharp-hours
line: 7.g patterns
backtest: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d1_day-long-fade-of-sharp-hours_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: In the last hour before the 00:00 UTC funding settlement, a coin continues the direction of its 24-hour return. The larger that 24-hour return relative to the coin's hourly volatility over the past 24 hours, the larger the move in that hour.
Consequence: A trader already positioned with a coin's strong 24-hour move would hold through the hour before the 00:00 UTC settlement, and would refuse to fade a strong trend in that hour.
Why:
- F1: In the hour just before the 00:00 UTC funding settlement (23:00 to 00:00), coins continue their 24-hour move rather than lean against it. The against-trend return is −5.01 bp (t −6.21, n 17,215), the most extreme of the 24 hours. The continuation is graded by the 24-hour move measured in hourly volatility: +0.05 bp in the smallest |z24| quintile, then 1.80, 5.13 and 5.31 bp, and +12.98 bp in the largest (t 5.93, n 3,390). This contradicts the brief's claim of a pre-settlement fade.
- F2: The 23:00 continuation holds on every coin: BTC +4.77 bp (t 3.40), ETH +5.33 (t 3.09), LTC +5.06 (t 2.62), XMR +4.19 (t 2.19), XRP +6.85 (t 3.13) and ZEC +3.83 (t 1.49). It is concentrated in 2020 to 2022 (+10.1, +17.6 and +11.1 bp, t 3.7 to 5.8) and near zero or negative in 2018, 2019 and 2023 to 2025 (−3.3 bp, t −1.88 in 2025).
- F4: Outside 15:00, 16:00 and 21:00 to 23:00, the largest 24-hour moves partly reverse the next hour: −3.54 bp (t −6.91, n 65,825) in the top |z24| quintile, against −0.18 bp in the bottom quintile. Pooled over all those other hours, the against-trend return is only +0.99 bp (t 5.27).
