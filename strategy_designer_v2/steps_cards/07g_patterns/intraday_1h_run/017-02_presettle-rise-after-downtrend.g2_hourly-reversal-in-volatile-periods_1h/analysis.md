---
line: 7.g patterns
backtest: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods_1h
idea tested: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3679 USD
---
## Findings
- **F1:** The fade's edge before costs is far smaller than its costs: the gross gain is 0.000088 per bar against a fee of 0.000622 per bar, from turning over 0.58 of the book per bar. The book loses more on days the coin moves more, from -0.0093 per day in the quietest fifth of coin days to -0.0210 in the most volatile fifth.
- **F2:** The one-hour reversal is real and grows with the volatility level. The mean of -sign(last hour) × next hour rises from 0.000047 (t 1.8) in the lowest fifth of 24h-volatility-to-its-30-day-average to 0.000376 (t 6.6) in the highest fifth. The slope of next-hour excess return per unit of scaled move goes from +0.000006 to -0.000581 across the same fifths.
- **F3:** In high volatility, down hours reverse far more than up hours. In the top volatility fifth, down hours give 0.000572 (t 6.9, n 37,672) and up hours 0.000189 (t 2.4). In the lowest fifth, down hours continue slightly (-0.000074, t -2.0) while up hours still revert (0.000166, t 4.6).
- **F4:** The reversal of the scaled one-hour move lasts well beyond one hour on non-overlapping grids. After the bottom fifth of scaled moves, the excess return is +0.000749 (t 4.8, n 20,646) over 4h and +0.002362 (t 2.8, n 3,422) over 24h. After the top fifth it is -0.000494 (t -3.5) over 4h and -0.003228 (t -3.8, n 3,425) over 24h.
- **F5:** Larger multi-hour moves also revert over the next 24h on non-overlapping grids. After the bottom fifth of volatility-scaled 4h moves, the 24h excess return is +0.003466 (t 3.9, n 3,424), against -0.002018 (t -2.3) in the fourth fifth. After the bottom fifth of scaled 24h moves it is +0.003511 (t 3.8), with the upper fifths near -0.0016 (t about -1.9).
- **F6:** The brief's settlement mechanism does not show. In the hour before the 0, 8 and 16 UTC funding times, -sign(24h trend) × next hour is -0.000063 (t -1.2, n 51,529), against +0.000060 (t 3.4) in the other hours. The reversal is strongest at 11–13 UTC (hour 11: 0.000618, t 7.2), a block whose t is between 1.5 and 4.6 in every year 2018–2025.
- **F7:** The reversal has weakened over time, from 0.000365 (t 5.9) in 2018 and 0.000302 (t 6.2) in 2020 to 0.000079–0.000115 (t 1.9–3.6) in 2022–2025. Every coin shows it except ETH (0.000054, t 1.5); it is strongest in ZEC (0.000304, t 5.9) and LTC (0.000274, t 6.8).
- **F8:** Excess returns depend on the hour of day, beyond what testing 24 hours would produce by chance. The hours starting 20 and 21 UTC give +0.000483 (t 6.0) and +0.000374 (t 4.8); hours 13 and 2 UTC give -0.000418 (t -4.5) and -0.000339 (t -4.6).

## Ideas
- `017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.g1_four-hour-move-daily-reversal` (from F4, F5, F1): Over the next 24 hours, a coin moves against its last 4-hour move. The larger that move relative to the coin's usual hourly volatility, the larger the move back.
- `017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.g2_volatile-period-drop-rebound` (from F3, F2): When a coin's 24-hour volatility is high relative to its 30-day average, the coin rises over the next hour after a falling hour. The larger the fall relative to its usual hourly volatility, and the higher that volatility ratio, the larger the rise.
- `017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods.g3_daily-sell-off-next-day-rebound` (from F5, F4): Over the next 24 hours, a coin rises after a fall over its last 24 hours. The deeper that fall relative to its usual hourly volatility, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
