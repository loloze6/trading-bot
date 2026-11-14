---
line: 7.g patterns
backtest: 002-03_price-cross-above-long-sma_1d
idea tested: 002-03_price-cross-above-long-sma
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3292 USD
---
## Findings
- **F1:** Over 783 trades, those held 5 days or less lost on average (−6.2% net, 1.2% winners, for 244 trades of ≤1.5 days; −6.5% net, 6.7% winners, for 539 trades of 1.5–5 days), while the 204 trades held over 60 days made +60.7% net with 75% winners, so the book's gain comes from a few long holds and short stays above the average are mostly whipsaws.
- **F2:** After a large down day the next day rises more often than usual: 58.6% of next-day excess returns are positive after a day below −2.5 trailing 20-day standard deviations (n=268, mean +0.66%, t=1.67), and 59.6% after a day between −2.5 and −1.5 (n=638, mean +0.33%, t=1.58), against 48.5% after ordinary days (n=12,145).
- **F3:** After a large up day the next day rises less often than usual: 41.4% positive after a day above +2.5 standard deviations (n=319) and 44.9% after a day between +1.5 and +2.5 (n=691), against 48.5% after ordinary days, though the mean next-day excess is near zero (−0.08% and −0.03%).
- **F4:** Next-day excess return depends on the weekday of the bar: after Friday bars it is +0.30% (t=3.66, 51.7% positive, n=2,430) and after Thursday bars +0.21% (t=2.29), while after Wednesday bars it is −0.30% (t=−2.75) and after Monday bars −0.22% (t=−2.34).
- **F5:** The book's best and worst 1% of days (171 each, mean +27.7% and −22.5%) both come when the close sits far above its 200-day SMA (median distance 114% and 59%, against −1.5% on other days), with the forecast near its cap (19.7 and 15.1) and the trailing 20-day volatility near 0.079–0.080, against 0.042 on other days.
- **F6:** The distance above the 200-day SMA does not sort forward returns: across the ten distance deciles the 20-bar excess t-statistics all lie between −0.34 and 0.86, and on bars above the SMA only 42% of 20-bar returns beat the coin's mean.

## Ideas
- `002-03_price-cross-above-long-sma.g1_one-day-rebound-after-drops` (from F2): After a daily close that falls more than 1.5 times the coin's trailing 20-day standard deviation of daily returns, the next day's close is above that close more often than after ordinary days.
- `002-03_price-cross-above-long-sma.g2_next-day-fade-after-spikes` (from F3): After a daily close that rises more than 1.5 times the coin's trailing 20-day standard deviation of daily returns, the next day's close is below that close more often than after ordinary days.
- `002-03_price-cross-above-long-sma.g3_friday-into-saturday-crypto-drift` (from F4): A coin's close-to-close return from Friday's daily close to Saturday's daily close is higher than its average daily return.
- `002-03_price-cross-above-long-sma.g4_stretched-trends-swing-wider` (from F5, F6): When a coin's close sits far above its 200-day SMA, its daily returns swing about twice as wide in both directions as when it sits near or below the average.
- `002-03_price-cross-above-long-sma.g5_fresh-crosses-mostly-whipsaw` (from F1): Once a coin's close moves above its 200-day SMA, it usually falls back below within a few days, and only a minority of these moves become long runs above the average.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
