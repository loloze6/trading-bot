---
line: 7.a not observable
backtest: 001-01_rsi-high-extreme-reversal_1d
idea tested: 001-01_rsi-high-extreme-reversal
step 5: not observable
step 6: none
mode: one call
explorations: 1
cost: 0.1398 USD
---
## Findings
- **F1:** The test ran on one coin and one window only: BTC, w1, 2022, 120 daily bars. ETH and BNB never ran, so the plan's 3-coin design was reduced to 1 coin with 23 non-overlapping 5-bar grid points.
- **F2:** The situation is not rare within a window. 39 of 120 bars (32.5%) had a short forecast, 15 bars (12.5%) reached forecast ≤ −10 (mean recomputed RSI 64.0, against 33.0 on flat bars), and 9 bars sat at the −20 cap. The forecast's 10% quantile was −13.2.
- **F3:** The extreme bars come in clusters, not spread out. The 15 extreme bars form 3 runs of length 1, 2 and 12, so the 5-bar grid caught only 3 extreme cases (3 of 23 grid points, 13%), against the plan's minimum of 30.
- **F4:** The forecast is graded in the expected way. Mean RSI rises from 54.6 at forecasts in (−5, 0) to 59.1 at (−10, −5] and 64.0 at ≤ −10.
- **F5:** The outcome is large and fairly consistent across the few cases, but the count is too small. The 3 cases had a mean excess 5-bar return of −6.75% with a standard deviation of 6.35%, giving t = −1.84. The spread of all grid 5-bar returns was 7.6%.
- **F6:** The year was a bearish one (2022: mean RSI 41.6, only 32.5% of bars with RSI > 50, base 5-bar return −0.5%). Because the forecast is standardised over 60 days, extremes are relative, so a rate of about 3 grid cases per 120-bar coin-window should hold in other years. About 10 coin-windows would then reach 30 cases, and the default 6 coins over folds A–D give many more than that.

## Ideas
- `001-01_rsi-high-extreme-reversal.a1_rsi-high-extreme-5-day-reversal` (from F1, F2, F3, F4, F5, F6): For a coin whose 14-day RSI is above 50, the higher that reading stands relative to its own past 60 days, the larger the coin's fall over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
