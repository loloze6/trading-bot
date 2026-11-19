---
line: 7.g patterns
backtest: 016-04_down-jump-price-reversal_1h
idea tested: 016-04_down-jump-price-reversal
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4410 USD
---
## Findings
- **F1:** The book lost because of churn, not because of the forecast. Mean daily book return was -0.00187 against +0.00119 for holding the coins. The 58,910 trades had a median length of 4 hours and turned the book over 1.5–2.7 times a day. Fees cost 0.0016–0.0024 a day per coin, while the gross gain per day was only -0.0004 to +0.0007.
- **F2:** Over the next 24 hours, coins revert their last 24-hour move scaled by volatility. On the non-overlapping 24-hour grid, the 24-hour return in units of 7-day hourly volatility has a slope of -0.00198 on the next-24h excess return (t -5.12, n 17,102). The slope is negative in every coin (t -1.61 to -3.53) and in both halves of the windows (w1–w12 t -3.92, w13–w24 t -3.43). The last single hour alone gives slope -0.00179 (t -5.18).
- **F3:** The same 24-hour reversal depends on how volatile the coin is relative to its usual level. With an interaction term, the scaled 24-hour return has coefficient +0.011 (t 12.7) and its product with relative volatility (7-day vol over the coin's mean vol) has -0.0131 (t -17.0). So reversal appears only once volatility is above about 0.83 of its usual level and deepens as volatility rises.
- **F4:** Over the next 3 days, coins that rose over the past 3 days kept rising more when the rise was efficient (net move over the sum of absolute hourly moves). The slope on efficiency was 0.056 (t 3.30, n 2,865) and is positive in 5 of 6 coins (t 1.0–1.7). By window, it is t 1.29 in w1–w12 and t 3.19 in w13–w24. After controlling for the rise's size and volatility, it is t 1.54. In the top tercile of rises, inefficient rises lost -3.2% excess and efficient ones gained +1.1%.
- **F5:** The tested measure, the share of a fall carried by its 3 largest hourly losses, explains nothing about the next 3 days (slope t -0.62 on falls, n 2,669). Volume concentration in the 3 biggest hours also adds nothing (t 0.60 on falls, t -1.75 on rises).
- **F6:** Choppy falls rebounded more than steady falls.
- **F7:** The UTC hours 20 and 21 are followed by positive next-hour returns: +0.049% and +0.038% (t 6.04 and 5.00).

## Ideas
- `016-04_down-jump-price-reversal.g1_volatile-regime-daily-move-reversal` (from F2, F3): The larger a coin's 24-hour return measured in units of its past 7-day hourly volatility, the more it moves the opposite way over the next 24 hours. This reversal is stronger the higher the coin's past 7-day volatility stands relative to its own usual level.
- `016-04_down-jump-price-reversal.g2_efficient-rallies-keep-rising` (from F4, F5): When a coin has risen over the past 3 days, the larger the share of its hourly path that went into the net rise (net 3-day move over the sum of absolute hourly moves), the more it rises over the next 3 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
