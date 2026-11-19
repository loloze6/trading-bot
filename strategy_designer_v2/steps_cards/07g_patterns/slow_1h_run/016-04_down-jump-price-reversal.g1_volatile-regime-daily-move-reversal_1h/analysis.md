---
line: 7.g patterns
backtest: 016-04_down-jump-price-reversal.g1_volatile-regime-daily-move-reversal_1h
idea tested: 016-04_down-jump-price-reversal.g1_volatile-regime-daily-move-reversal
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3399 USD
---
## Findings
- **F1:** The fade's 24-hour forecast is real, but the book loses to costs. On the 24-bar grid the forecast earns a pooled mean of 0.00226 (t 4.89, n 17,246), while fees per day (0.0021 to 0.0035 per coin, from 1.9 to 3.1 turns of the book a day) are larger than gross gains per day (-0.0009 to +0.0025), so every coin's book falls (-0.0010 to -0.0032 per day).
- **F2:** Nearly all of the reversal comes from the high-volatility tercile, where the 7-day volatility is well above its 30-day mean. Down-moves (bottom fifth of 24-hour return in volatility units) then rebound by 0.0124 excess over the next 24 hours (t 5.65, n 1,005), and up-moves fall back by 0.0047 (t 2.45, n 1,039). In the low and middle terciles the reversal is between -0.0001 and 0.0017 with every |t| < 1.3. The regression term for scaled move × volatility ratio has t -9.26.
- **F3:** The reversal is lopsided toward falls. The bottom fifth of scaled 24-hour moves is followed by +0.0041 excess over the next 24 hours (t 4.25, n 3,308), while the top fifth is followed by only -0.0019 (t -2.19, n 3,305).
- **F4:** After the first day, large moves continue rather than reverse. Over hours 24 to 96 after the bar, the top fifth of scaled 24-hour moves gains a further 0.0046 excess (t 3.77, n 3,254). The 24-hour forecast's edge fades to t 0.06 at 72 hours and t -1.27 at 168 hours.
- **F5:** Against the brief, falls with evenly spread volume rebound most, and falls built on a volume burst rebound least. In the lowest tercile of volume concentration (largest hour's share of 24-hour volume), bottom-fifth moves rebound 0.0080 (t 3.86, n 977); in the highest tercile they rebound 0.0006 (t 0.43, n 1,240). The regression term for scaled move × volume concentration has t +3.36, so a volume burst weakens the reversal.

## Ideas
- `016-04_down-jump-price-reversal.g1_volatile-regime-daily-move-reversal.g1_volatile-regime-selloff-rebound` (from F2, F3, F1): The larger a coin's 24-hour fall, measured in units of its past 7-day hourly volatility, the more it rises over the next 24 hours. The rebound is larger the higher the coin's 7-day volatility stands above its own 30-day average.
- `016-04_down-jump-price-reversal.g1_volatile-regime-daily-move-reversal.g2_delayed-continuation-after-shocks` (from F4): The larger a coin's 24-hour return, measured in units of its past 7-day hourly volatility, the more the coin keeps moving in the same direction over the three days that start one day after the move.
- `016-04_down-jump-price-reversal.g1_volatile-regime-daily-move-reversal.g3_even-volume-selloffs-rebound` (from F5, F3): The more evenly a coin's volume is spread across the hours of a 24-hour fall, the more the coin rises over the next 24 hours, for falls of the same size measured in units of its 7-day hourly volatility.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
