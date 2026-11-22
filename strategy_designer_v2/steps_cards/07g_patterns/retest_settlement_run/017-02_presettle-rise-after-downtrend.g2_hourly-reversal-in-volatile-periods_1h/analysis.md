---
line: 7.g patterns
backtest: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods_1h
idea tested: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3851 USD
---
## Findings
- **F1:** The tested hourly fade cannot pay. Its move is +0.01 % per case, a tenth of the 0.19 % a trade costs, and the book traded 20.42 times a day for a Sharpe of -11.93. The reversal itself is real only in the smaller coins: the 1h slope t is -5.0 for LTC, -6.2 for XMR, -5.9 for XRP and -7.8 for ZEC, against -1.1 for BTC and +0.1 for ETH.
- **F2:** A full day's move also reverses over the next day, mostly when the coin's 24h volatility is high against its 30-day mean. On non-overlapping 24h cases, the slope of the next 24h excess return on the past 24h move (in volatility units) is -50.7 bp per unit with t -6.25 in the top tercile of that ratio (5221 cases). It is -8.1 bp (t -1.14) in the middle tercile and +9.1 bp (t +1.34) in the bottom tercile.
- **F3:** The 24h fade is graded and, for larger moves, bigger than the cost of a trade. The faded next-day move rises from -6.9 bp in the smallest-move quintile to +11.4 bp in the middle one, +39.5 bp (t 4.37) in the fourth and +19.0 bp (t 2.01) in the largest, against 0.19 % per trade. Over all 15662 cases it is +12.4 bp, a pure number of about 0.003 of the usual 497 bp daily move.
- **F4:** The 24h reversal is not uniform over time. Its slope is negative in every coin, with t from -1.1 (ZEC) to -3.2 (XMR). By year it is negative from 2018 to 2023 (t -3.4, -2.2, -0.9, -2.8, -1.8, -2.1) and absent in 2024 and 2025 (t +0.17, +0.28).
- **F5:** Across the 24 hours of the day, the hour after the 20:00 UTC close is the strongest at +4.8 bp excess (t 5.98), followed by the next one at +3.7 bp (t 4.85). The two-hour excess from the 20:00 close is positive in all six coins (+7.3 to +9.6 bp, t 2.6 to 4.1), in 7 of 8 years (2022: -5.5 bp, t -1.8) and in both halves of the year (t 4.2 and 7.0). This survives the 24 hours compared.
- **F6:** The hour after the 13:00 UTC close falls by -4.2 bp excess (t -4.46). It is strongest in 2021 (-17.7 bp, t -5.0) and near zero in 2022 to 2025, so it is less stable than F5.
- **F7:** The brief's settlement clock does not stand out. Before the 23/07/15 UTC settlements, the 2-hour return runs with the 24h trend rather than against it (-1.4 bp against, t -2.1), opposite to the brief's claim. After them it follows the trend by +1.8 bp (t 2.7). At the off-settlement hours 03/11/19, the post-hour move instead goes against the trend (-4.4 bp, t -6.8), so the pattern is not specific to settlement times.

## Ideas
- `017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.g1_daily-fade-in-volatility-spikes` (from F2, F3, F4, F1): Over the next 24 hours, a coin moves against its last 24-hour return, and the larger that return relative to its usual daily volatility, the larger the reversal, more strongly the higher its 24-hour volatility stands above its 30-day average.
- `017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.g2_late-evening-utc-drift` (from F5): Over the two hours after the 20:00 UTC close, a coin rises more than its usual drift, by an amount that grows with its 24-hour volatility.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
