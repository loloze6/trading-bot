---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d2_buy-sharp-volatile-hourly-falls
line: 7.g patterns
backtest: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d2_buy-sharp-volatile-hourly-falls_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's 24-hour volatility is raised against its 30-day average, its return over the next 24 hours runs against its return over the past 24 hours. The larger the past 24-hour move in units of the coin's usual volatility, and the higher the volatility ratio, the larger the move back.
Consequence: In volatile periods, a trader would buy a coin after a large 24-hour fall and sell it after a large 24-hour rise, holding for a day; the 44–124 bp moves per case are well above the 0.19 % cost of a trade.
Why:
- F1: When a coin's 24-hour volatility is in the top fifth relative to its own 30-day average, its next-24-hour excess return is +44.4 bp (t 3.93, 3133 non-overlapping cases), against −7 to −18 bp in the other four fifths. Inside that top fifth the effect grows with the volatility ratio, by quarter: +7.6, +22.8, +67.6 (t 2.91) and +79.9 bp (t 2.91). It is positive in all six coins (+16.6 to +94.8 bp) and in 6 of 8 years.
- F2: Inside that high-volatility fifth, the next 24 hours run against the past 24 hours. After the largest 24-hour falls, measured in 30-day-average volatility units, the excess is +123.8 bp (1152 cases). After the largest 24-hour rises it is −47.4 bp (1079 cases). The correlation is −0.117 over 3133 cases. In low-volatility periods the pattern is absent or reversed (lowest fifth: −45.7 bp after falls, +16.1 bp after rises).
- F3: The sharpest single-hour falls, the tested idea's own situation, are followed by +65.6 bp of 24-hour excess (bottom decile, t 4.23, 1567 cases). The next decile gives only +15.3 bp (t 1.23) and the rest are flat or negative. So the effect lives in the extreme tail and in high volatility (F1), and the strategy's bets measured −0.01 % per case.
