---
line: 7.d not profitable
backtest: 016-04_down-jump-price-reversal.g1_volatile-regime-daily-move-reversal_1h
idea tested: 016-04_down-jump-price-reversal.g1_volatile-regime-daily-move-reversal
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3182 USD
---
## Findings
- **F1:** The book loses because of fees, not because the forecast is wrong: before fees it earns +0.00031 a day (t 1.49), but it pays 0.00262 a day in fees on a turnover of 2.42 of the book per day, which leaves a mean daily return of −0.0023 and a Sharpe of −2.30.
- **F2:** The same forecast, read only every 24 hours and held for 24 hours, earns +0.00223 per day before fees (t 4.80, 17,246 independent cases) on a turnover of only 1.29 a day, so fees would be about 0.0014 (at the book's 0.0011 per unit of turnover); the hourly book throws this gain away because the forecast's autocorrelation is 0.94 one hour ahead but −0.02 to −0.09 one day ahead, and its sign flips on about 10% of hours.
- **F3:** The gain sits entirely in the highest third of volatility ratio (7-day volatility over its 30-day average): on the 24-hour grid that third earns +0.0077 per case, against +0.0001 for the middle third and −0.0007 for the lowest; in the hourly book it earns +0.00197 a day before fees, against −0.00083 in the lowest third.
- **F4:** Inside the high-volatility third, long positions after falls catch a signed 24-hour return of +0.0078 (n 2,467), against +0.0022 for short positions after rises (n 2,654); in the low-volatility third, short positions lose 0.0021 (n 2,582) because the coins drift up.
- **F5:** Gain grows with forecast size only at the daily scale: on the 24-hour grid the top fifth of |forecast| earns +0.0073 against −0.0002 for the bottom fifth, but in the hourly book the top fifth earns −0.0002 a day before fees, so the hourly re-sizing destroys the graded edge.

## Ideas
- `016-04_down-jump-price-reversal.g1_volatile-regime-daily-move-reversal.d1_reversal-only-in-high-volatility` (from F1, F3, F5): The larger a coin's 24-hour return measured in units of its past 7-day hourly volatility, the more it moves the opposite way over the next 24 hours, only while the coin's 7-day volatility stands above its own 30-day usual level, and the further above it stands, the stronger the reversal.
- `016-04_down-jump-price-reversal.g1_volatile-regime-daily-move-reversal.d2_daily-paced-move-reversal` (from F1, F2, F5): The larger a coin's 24-hour return measured in units of its past 7-day hourly volatility, the more it moves the opposite way over the next 24 hours, with the reversal unfolding across the whole following day, so that the move as it stands at a day's close carries it rather than its hour-to-hour changes.
- `016-04_down-jump-price-reversal.g1_volatile-regime-daily-move-reversal.d3_volatile-fall-rebound` (from F3, F4): The larger a coin's 24-hour fall measured in units of its past 7-day hourly volatility, the more it rises over the next 24 hours, and the more so the higher its 7-day volatility stands above its own 30-day usual level.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
