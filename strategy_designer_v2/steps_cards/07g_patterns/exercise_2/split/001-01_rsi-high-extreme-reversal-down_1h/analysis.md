---
line: 7.g patterns
backtest: 001-01_rsi-high-extreme-reversal-down_1h
idea tested: 001-01_rsi-high-extreme-reversal-down
step 5: inconclusive
step 6: not profitable enough
mode: analyst then deducer
explorations: 2
cost: 0.4087 USD
---
## Findings
- **F1:** The book's losses come mostly from trading costs rather than from direction. The positions' gross P&L summed only -0.36 (BTC) and -0.56 (ETH) in log terms, while the book summed -2.96 and -3.63. Turnover was about 2,950 and 2,860 allocation units per coin, and each trade paid about 0.28–0.30% in commission against a mean gross result of -0.47% to -0.57%.
- **F2:** Trade results depend strongly on how long the trade is held. Trades of 3 hours or less earned +0.33% gross (n=3452). Trades of 6–17 hours lost -0.70% (n=1562), and trades longer than 17 hours lost -2.85% (n=1464).
- **F3:** The trade P&L is heavily negatively skewed. Shorts win 58–62% of the time with a median of +0.08%. But the 5th percentile is -5.06% against a 95th percentile of +1.34%, and the worst 10% of trades account for 125% of the total gross loss.
- **F4:** The weakest entries are held longest. Trades entered at the smallest forecasts (-5.9 to -2.0) last 19.9 hours on average, against 8.9 hours for the strongest (≤ -11.3), and they have the lowest win rate (57% vs 60%).
- **F5:** Forward returns do not fall steadily as RSI gets more extreme. The excess 12-bar return is +0.021% in the most extreme forecast bin (≤ -10, n=7375), -0.025% for -10..-4, +0.133% for -4..-1, and -0.025% at a zero forecast.
- **F6:** The extreme-RSI reading behaves differently depending on volatility (non-overlapping 12-bar blocks). In the lowest 24h-volatility tercile, extreme bars are followed by an excess +0.28% (t=1.96, n=157), which is continuation. In the middle tercile they are followed by -0.19% (t=-1.27, n=215), and in the high tercile by -0.14% (t=-0.77, n=226).
- **F7:** The book lost in all 12 coin-windows, whether the coin fell or rose. It lost most in the rising windows w4 and w6 (coin +0.32 to +0.57, book -0.69 to -1.12), where it was short on 69–76% of bars. Even in falling windows it lost (for example ETH w2: coin -0.57, book -0.60).
- **F8:** The book's largest losses come at near-maximum short size in volatile bars. In its worst 1% of bars the mean allocation is -2.06 and 24h volatility is 0.81%, against about 0.55% on all bars. The bar before averaged +61 bp, and the price kept drifting up afterwards (+2.6, +5.0 and +5.2 bp at 1, 3 and 12 bars).
- **F9:** The book loses more as volatility rises. Mean absolute allocation goes from 0.42 in the lowest 24h-volatility quintile to 0.53 in the highest, and the book's mean hourly return worsens from -1.1 bp to -2.5 bp.
- **F10:** Large single-hour moves carry no follow-through and no reversal over the next 12 bars. After moves beyond ±2 or ±3 standard deviations, the forward 12-bar excess return stays between -0.00001 and +0.0013, with every |t| below 0.3.
- **F11:** One hour-of-day effect holds across both coins and both years. Returns at UTC hour 1 average -3.95 bp (t=-2.10) and are negative in all four coin-year cells (-1.4 to -6.3 bp). The positive effects at hour 20 (+4.39 bp, t=2.36) and hour 22 (+3.79 bp, t=2.17) are not consistent: hour 20 is -2.2 bp for ETH in 2023, and hour 22 is about 0 in 2022.

## Ideas
- `001-01_rsi-high-extreme-reversal-down.g1_calm-market-high-rsi-continuation` (from F6, F9): When a coin's 24-hour volatility is in its lowest third and its 14-hour RSI sits at a high extreme, the price keeps rising over the next 12 hours by more than its usual drift.
- `001-01_rsi-high-extreme-reversal-down.g2_persistent-high-rsi-continues` (from F2, F4, F7, F3): Once a coin's 14-hour RSI has stayed above 50 for many hours in a row, the price keeps rising over the following 12 hours more than its usual drift.
- `001-01_rsi-high-extreme-reversal-down.g3_weak-01-utc-hour` (from F11): A coin's return over the hour from 01:00 to 02:00 UTC is below its average hourly return.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
