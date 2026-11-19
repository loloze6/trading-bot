---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-04_postsettle-decline-after-downtrend.c2_off-settlement-rebound-after-falls
line: 7.g patterns
backtest: 017-04_postsettle-decline-after-downtrend.c2_off-settlement-rebound-after-falls_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: For a coin, the larger its last 1-hour return relative to its own hourly volatility over the past 24 hours, the larger the move the opposite way over the next 2 hours. A sharp hourly drop is followed by a rise, and a sharp hourly jump by a fall.
Consequence: A trader should fade an outsized single-hour move for a couple of hours, and should refuse to chase it.
Why:
- F1: The last hour's move reverses over the next 2 hours, measured on 41,310 non-overlapping 2-bar cases per quintile of the last 1-hour return divided by its 24-hour volatility. The quintile with the largest falls is followed by +6.74 bp of excess return (t 8.3). The quintile with the largest rises is followed by −4.54 bp (t −6.1), and the three middle quintiles fall in order between them (+2.53, −1.84, −3.42 bp).
- F2: This reversal is in every coin and nearly every period. The bottom-minus-top quintile spread is positive in all 6 coins (BTC 2.95, ETH 2.80, LTC 12.9, XMR 14.5, XRP 12.3, ZEC 23.2 bp), in 72% of the coin-windows, and in every year from 2018 to 2025 (from 1.8 bp in 2022 to 31.0 bp in 2018).
- F4: The reversal fades with a longer past move. The correlation with the next 2-hour excess return is −0.025 for the scaled 1-hour return, −0.019 for the 3-hour return and −0.015 for the 6-hour return. Measured by 72-hour depth, as the strategy does, deep falls at off-settlement closes are followed by −1.41 bp (t −1.17, n 15,853).
