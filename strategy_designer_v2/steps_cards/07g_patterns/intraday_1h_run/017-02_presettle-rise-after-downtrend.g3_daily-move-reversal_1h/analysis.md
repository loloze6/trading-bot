---
line: 7.g patterns
backtest: 017-02_presettle-rise-after-downtrend.g3_daily-move-reversal_1h
idea tested: 017-02_presettle-rise-after-downtrend.g3_daily-move-reversal
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3625 USD
---
## Findings
- **F1:** The 24-hour reversal works only when recent volatility is high for the coin. Split by the coin's 168-hour volatility relative to its 720-hour median, the reversal slope has t=7.53 in the top fifth (relative volatility 1.81) and t=3.20 in the fourth, but is slightly negative in the three lower fifths (t = -0.88, -0.13, -0.78). A predictor of the negated z-score times relative volatility reaches t=8.23, against t=5.20 for the negated z-score alone (n=15230 non-overlapping 24-hour cases).
- **F2:** In the high-relative-volatility fifth the reversal holds over time: the slope is positive in all 8 years and has t≥2.1 in 6 of them (2018 3.43, 2019 3.76, 2020 2.39, 2021 4.79, 2023 2.12, 2025 3.21). 2022 (t=1.23) and 2024 (t=0.33) are weaker.
- **F3:** The reversal is almost entirely a rebound after falls. After a 24-hour fall the slope is 0.0045 with t=4.88 (n=8179). After a rise it is 0.0005 with t=0.61 (n=8491). In the forecast quintiles the strongest long quintile earns +30.2 bp excess over the next 24 hours (t=3.21), while the strongest short quintile earns -11.8 bp (t=-1.45), so the short side adds little.
- **F4:** Coins rise in the hours starting 20:00 and 21:00 UTC: +5.45 bp (t=6.75) and +4.36 bp (t=5.66) per hour. These are the largest of the 24 hours, so they stand out even after testing every hour. In volatility units the rise is positive in all six coins (t from 2.11 for XRP to 4.43 for BTC), on all seven weekdays, and in 7 of 8 years. 2022 is the exception (t=-3.57).
- **F5:** The funding clock times show no distinctive behaviour. The hours just before and after 00, 08 and 16 UTC have normalised mean returns between -0.021 and +0.023, with |t| ≤ 2.8. That is no larger than at non-funding hours such as 02 (-2.77 bp, t=-3.80) or 13 (-3.56 bp, t=-3.80), so it does not support the brief's settlement mechanism.
- **F6:** Trading costs, not the forecast, sink the book. Mean gain before fees is +0.000066 per coin-day, fees are 0.0028 per coin-day, and turnover is 0.108 of the book per hour (11.1 trades per day). The result is a mean daily book return of -0.00274, against +0.00119 for holding the coin.

## Ideas
- `017-02_presettle-rise-after-downtrend.g3_daily-move-reversal.g1_volatile-drop-next-day-rebound` (from F1, F2, F3, F6): Over the next 24 hours, a coin rebounds after a 24-hour fall. The rebound is larger the deeper the fall in units of the coin's one-week hourly volatility, and larger still the higher that one-week volatility is relative to its one-month median.
- `017-02_presettle-rise-after-downtrend.g3_daily-move-reversal.g2_volatility-weighted-daily-reversal` (from F1, F2): Over the next 24 hours, a coin moves against its 24-hour return. The size of the reversal grows with that return measured in one-week volatility units multiplied by the ratio of the coin's one-week hourly volatility to its one-month median.
- `017-02_presettle-rise-after-downtrend.g3_daily-move-reversal.g3_late-evening-utc-drift` (from F4, F5): A coin rises over the two hours from 20:00 to 22:00 UTC, and the rise is larger the higher its one-week hourly volatility.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
