---
line: 7.g patterns
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal_1d
idea tested: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3371 USD
---
## Findings
- **F1:** The next-day reversal is concentrated in high-volatility days. In each coin's top tercile of 20-day volatility, the pooled slope of next-day excess return on the volatility-scaled one-day move is -0.00709 (t -8.26, n 5315). In the middle tercile it is t -0.62, and in the bottom tercile it is +0.00127 (t +2.70). The continuous move × volatility-rank interaction has t -9.32 (n ≈ 15,940).
- **F2:** The high-volatility reversal holds coin by coin and year by year. All six coins have a negative slope there: XMR t -5.44, ETH -4.21, BTC -4.16, ZEC -3.10, LTC -2.50 and XRP -1.87 (886 bars each). Seven of eight years are negative, with t from -1.96 to -4.88; 2025 is the exception at t +0.28 (n 427).
- **F3:** The book's own gain follows the volatility split. Position × next-day return averages +0.00231 per bar in the high-volatility tercile (t 7.15, n 5315) and -0.000868 in the low-volatility tercile (t -2.19, n 5315). The book's overall loss therefore comes from fading moves on calm days.
- **F4:** In the high-volatility tercile, the rebound after falls is larger than the drop after rises. Days with a scaled move of -1.5 or less are followed by a +2.39% next-day excess return (t 4.90, n 276), and days between -1.5 and -0.5 by +0.82% (t 4.43, n 1090). Days between +0.5 and +1.5 are followed by -0.76% (t -4.28, n 1056), but days above +1.5 by only -0.40% (t -1.06, n 355).
- **F5:** Reversal also strengthens with volatility expansion. By tercile of 20-day over 60-day volatility, the slope t goes from +0.84 (lowest) to -2.89 (middle) to -4.91 (highest), with about 4,350 bars per tercile.
- **F6:** The reversal is stronger below a coin's 50-day average (slope t -5.01, n 6732) than above it (t -1.52, n 6472).
- **F7:** On low-volatility days, moves continue the next day instead. The pooled slope is positive (t +2.70), and it is positive for BTC (t 2.26), ETH (t 2.05), ZEC (t 1.84), XRP (t 0.61) and LTC (t 0.33); XMR is the exception at t -0.21. The per-coin values are weak on their own.

## Ideas
- `002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal.g1_high-volatility-fall-rebound` (from F1, F2, F3, F4): When a coin's 20-day volatility is high compared with its own past levels, the larger its one-day fall relative to its usual daily move over the past 20 days, the larger its rise over the next day. The higher that volatility, the stronger the rebound.
- `002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal.g2_reversal-under-volatility-expansion` (from F1, F5): The more a coin's 20-day volatility exceeds its 60-day volatility, the more its next-day return runs opposite to its one-day move, in proportion to that move's size against the coin's usual daily move.
- `002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal.g3_downtrend-one-day-reversal` (from F6, F1): When a coin trades below its 50-day average, the larger its one-day move relative to its usual daily move over the past 20 days, the larger the opposite move over the next day.
- `002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal.g4_calm-market-one-day-continuation` (from F7, F3): When a coin's 20-day volatility is low compared with its own past levels, the larger its one-day move relative to its usual daily move, the further it moves the same way over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
