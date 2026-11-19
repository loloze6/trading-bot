---
line: 7.g patterns
backtest: 016-07_up-volume-burst-reversal.g1_efficient-rises-keep-rising_1h
idea tested: 016-07_up-volume-burst-reversal.g1_efficient-rises-keep-rising
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5501 USD
---
## Findings
- **F1:** Over the next 24 hours, a coin gives back part of its past day's move. Regressing the next 24-hour excess return on the past 24-hour return, scaled by 30-day hourly volatility, gives a slope t of -5.59 (n=12926, non-overlapping 24h grid). The past 6-hour version gives t -4.82 and the past 12-hour version t -4.69. After a past-6h z of -2 or less, the next 24h excess is +0.74% (t 2.00, n=339); after a z of +2 or more it is -0.71% (t -2.08, n=313).
- **F2:** The 24-hour reversal is broad across coins and years. The slope is negative in all six coins (t from -0.51 for LTC to -3.30 for XMR) and in 7 of 8 years (2018 t -4.46, 2019 t -2.66, 2020 t -2.87; 2024 is the exception at t +1.64). In every coin, the next-24h excess after a 6h fall is above the excess after a 6h rise (BTC +0.13% vs -0.12%, ETH +0.29% vs -0.26%).
- **F3:** A sharp hourly fall is followed by a graded next-hour bounce. After a 1-hour return z of -1 to -2 (scaled by 30-day hourly volatility), the next hour gains +0.062% (t 7.56, n=22832). After -2 to -4 it gains +0.075% (t 3.77, n=6915), and after -4 or less +0.25% (t 3.12, n=1076). After a z between -1 and +1 the next hour returns only +0.002% (t 1.08). The bounce after z<-1 is positive in all six coins (t 1.95 to 4.90) and in 7 of 8 years (2022 is -0.019%, t -1.01).
- **F4:** The book's loss comes mainly from costs, not from the forecast's direction. Turnover of 0.65 to 1.22 of the book per day costs 0.08% to 0.14% per day in fees. Gross gain before fees is about 0.10% to 0.13% per day in BTC, ETH and XRP, 0.02% to 0.03% in LTC and ZEC, and -0.06% in XMR. The plan's own measure, the efficiency ratio among rises, has a weak overall rank link to the next 72h excess (Spearman 0.044). Only its top quintile stands out (+1.23%, t 3.02, n=574), and that top quintile is negative in 2019 and 2022.
- **F5:** Next-hour returns are higher after the 20:00 and 21:00 UTC bars: +0.045% (t 5.02) and +0.057% (t 6.39), against near-zero means in most other hours. This holds in all six coins (t 2.98 to 4.44) and in 7 of 8 years (2022 is -0.022%, t -1.44). It is a fixed time-of-day effect with no graded situation, so it does not support a graded idea here.

## Ideas
- `016-07_up-volume-burst-reversal.g1_efficient-rises-keep-rising.g1_one-day-volatility-scaled-reversal` (from F1, F2): The larger a coin's past 24-hour return relative to its own usual hourly volatility over the past 30 days, the more the coin moves in the opposite direction over the next 24 hours.
- `016-07_up-volume-burst-reversal.g1_efficient-rises-keep-rising.g2_hourly-crash-bounce` (from F3): The larger a coin's 1-hour fall relative to its own usual hourly volatility over the past 30 days, the more the coin rises over the next hour.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
