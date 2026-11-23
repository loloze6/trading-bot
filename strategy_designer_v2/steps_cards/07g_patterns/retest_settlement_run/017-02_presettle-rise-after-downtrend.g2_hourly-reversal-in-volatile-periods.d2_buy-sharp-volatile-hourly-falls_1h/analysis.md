---
line: 7.g patterns
backtest: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d2_buy-sharp-volatile-hourly-falls_1h
idea tested: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d2_buy-sharp-volatile-hourly-falls
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4092 USD
---
## Findings
- **F1:** When a coin's 24-hour volatility is in the top fifth relative to its own 30-day average, its next-24-hour excess return is +44.4 bp (t 3.93, 3133 non-overlapping cases), against −7 to −18 bp in the other four fifths. Inside that top fifth the effect grows with the volatility ratio, by quarter: +7.6, +22.8, +67.6 (t 2.91) and +79.9 bp (t 2.91). It is positive in all six coins (+16.6 to +94.8 bp) and in 6 of 8 years.
- **F2:** Inside that high-volatility fifth, the next 24 hours run against the past 24 hours. After the largest 24-hour falls, measured in 30-day-average volatility units, the excess is +123.8 bp (1152 cases). After the largest 24-hour rises it is −47.4 bp (1079 cases). The correlation is −0.117 over 3133 cases. In low-volatility periods the pattern is absent or reversed (lowest fifth: −45.7 bp after falls, +16.1 bp after rises).
- **F3:** The sharpest single-hour falls, the tested idea's own situation, are followed by +65.6 bp of 24-hour excess (bottom decile, t 4.23, 1567 cases). The next decile gives only +15.3 bp (t 1.23) and the rest are flat or negative. So the effect lives in the extreme tail and in high volatility (F1), and the strategy's bets measured −0.01 % per case.
- **F4:** The coins rise in the two hours that start at 21:00 UTC. The bars opening at 20:00 and 21:00 UTC are followed by next-hour excess of +4.8 bp (t 5.98) and +3.7 bp (t 4.85). This holds in all six coins (t 2.5 to 3.9) and in 7 of 8 years.
- **F5:** The F4 rise grows with the coin's 24-hour volatility against its 30-day average: +1.2 bp (t 1.45) in the lowest fifth and +10.0 bp (t 5.06) in the highest.
- **F6:** The book is mostly the coin's own rise. Its daily return on the coin's has slope 0.70 with r² 0.77 over 17381 coin-days, and an intercept of only 2.3 bp a day. It holds a position on 99 % of coin-days, with mean allocations of 0.62 to 1.11. Its Sharpe edge over holding (+0.08) does not come from the tested idea.
- **F7:** Two further clock patterns are too uneven across years to carry an idea:

## Ideas
- `017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d2_buy-sharp-volatile-hourly-falls.g1_volatile-period-daily-reversal` (from F1, F2, F3): When a coin's 24-hour volatility is raised against its 30-day average, its return over the next 24 hours runs against its return over the past 24 hours. The larger the past 24-hour move in units of the coin's usual volatility, and the higher the volatility ratio, the larger the move back.
- `017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.d2_buy-sharp-volatile-hourly-falls.g2_late-us-session-volatile-rise` (from F4, F5): A coin rises over the two hours after 21:00 UTC, and the higher its 24-hour volatility against its 30-day average, the larger that rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
