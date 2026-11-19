---
line: 7.g patterns
backtest: 017-04_postsettle-decline-after-downtrend.c2_off-settlement-rebound-after-falls_1h
idea tested: 017-04_postsettle-decline-after-downtrend.c2_off-settlement-rebound-after-falls
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3372 USD
---
## Findings
- **F1:** The last hour's move reverses over the next 2 hours, measured on 41,310 non-overlapping 2-bar cases per quintile of the last 1-hour return divided by its 24-hour volatility. The quintile with the largest falls is followed by +6.74 bp of excess return (t 8.3). The quintile with the largest rises is followed by −4.54 bp (t −6.1), and the three middle quintiles fall in order between them (+2.53, −1.84, −3.42 bp).
- **F2:** This reversal is in every coin and nearly every period. The bottom-minus-top quintile spread is positive in all 6 coins (BTC 2.95, ETH 2.80, LTC 12.9, XMR 14.5, XRP 12.3, ZEC 23.2 bp), in 72% of the coin-windows, and in every year from 2018 to 2025 (from 1.8 bp in 2022 to 31.0 bp in 2018).
- **F3:** The reversal grows with volatility. By 24-hour volatility tercile, the bottom-minus-top spread is 1.3 bp (corr t −1.07) in calm bars, 5.0 bp (t −2.58) in middle bars and 29.7 bp (t −11.9) in volatile bars. In the volatile tercile the correlation of the scaled 1-hour return with the next 2 hours is negative in all 6 coins (−0.024 to −0.055, about 11,000 cases each).
- **F4:** The reversal fades with a longer past move. The correlation with the next 2-hour excess return is −0.025 for the scaled 1-hour return, −0.019 for the 3-hour return and −0.015 for the 6-hour return. Measured by 72-hour depth, as the strategy does, deep falls at off-settlement closes are followed by −1.41 bp (t −1.17, n 15,853).
- **F5:** The book loses money because of fees, not because its timing is wrong. Its gross gain per bar is 0.02 to 0.32 bp in every coin, against fees of 0.65 to 0.88 bp per bar, at 2.34 trades per day.
- **F6:** Bars closing at 21 UTC are followed by +7.9 bp of excess 2-hour return (t 6.4, n 12,600), the largest of the 24 close hours. This holds in all 6 coins (t 1.8 to 3.3), in 7 of 8 years and in 73% of coin-windows. It is a fixed clock-time effect with no graded situation, so it suggests no idea here.

## Ideas
- `017-04_postsettle-decline-after-downtrend.c2_off-settlement-rebound-after-falls.g1_one-hour-move-reverses` (from F1, F2, F4): For a coin, the larger its last 1-hour return relative to its own hourly volatility over the past 24 hours, the larger the move the opposite way over the next 2 hours. A sharp hourly drop is followed by a rise, and a sharp hourly jump by a fall.
- `017-04_postsettle-decline-after-downtrend.c2_off-settlement-rebound-after-falls.g2_volatile-hour-spike-reversal` (from F3, F1, F5): When a coin's hourly volatility over the past 24 hours is high, its last 1-hour return, scaled by that volatility, is followed over the next 2 hours by an opposite move that grows with the size of that hour's move. The reversal is several times larger than in calm periods.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
