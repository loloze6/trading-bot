---
line: 7.d not profitable
backtest: 002-01_sma-golden-cross-upward-drift_1d
idea tested: 002-01_sma-golden-cross-upward-drift
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3555 USD
---
## Findings
- **F1:** The bars just after the forecast turns positive lose money: in the first 20 days of a long stretch the book's mean daily return is -0.000512 (Sharpe -0.34, n=2065) and the coin's is -0.000471, against 0.000993 for days 20–60 (n=3524) and 0.001657 for days 60–120 (n=2619, Sharpe 0.90); the weak forecast bucket 0–5 also earns -0.000011 a day (n=2154).
- **F2:** While long, the coin's own past 20-day return grades what follows: in the top quintile (above +18.9%) the book earns 0.002455 a day (Sharpe 1.52, n=1731) and the coin 0.005509 (t 3.69); in the middle quintile the book earns 0.000157 and in the bottom quintile 0.000102.
- **F3:** While long, bars near the coin's 60-day high (within 3.4%) earn the book 0.001762 a day (Sharpe 1.11, n=1881); the other drawdown quintiles earn between -0.000125 and 0.001094.
- **F4:** The deepest falls happen while the book is long: BTC fell -45.6% in 88 days while fully long (share long 1.00, mean forecast 15.2, coin -63%). ZEC fell -84.8%, XRP -59.6% and ETH -69.1%, with the book long 61–75% of those stretches and the coin falling 71–92%. This is what keeps Calmar at 0.20.
- **F5:** Holding beats the book because the flat bars still carry the coin's drift: on the 8454 bars with forecast 0 the coin averages 0.001295 a day (t 2.79) while the book earns 0.000018. Every coin's book mean (0.000108–0.000868) is below its coin mean (0.000670–0.001879).
- **F6:** The volatility sizing puts the smallest positions where the coin gains most: in the highest 20-day volatility quintile the coin earns 0.004961 a day (t 2.89) at a mean allocation of 0.33, while the lowest quintile earns 0.000591 at an allocation of 0.67.
- **F7:** Fees are not the cause: 905 trades average 5.64% gross and 5.54% net, with a mean commission of 0.11%, a median length of 39 days and 37% winners.

## Ideas
- `002-01_sma-golden-cross-upward-drift.d1_golden-cross-with-momentum` (from F2, F3, F4): While a coin's 50-day SMA is above its 200-day SMA, the coin keeps rising, further the larger the spread, only while its own recent return is strongly positive and its price stands near its recent high; the stronger the recent rise, the larger the gain that follows.
- `002-01_sma-golden-cross-upward-drift.d2_aged-cross-drift` (from F1): While a coin's 50-day SMA is above its 200-day SMA, the coin keeps rising, further the larger the spread, except in the early stretch just after the cross; the drift grows with the time the short average has stayed above the long one.
- `002-01_sma-golden-cross-upward-drift.d3_volatile-trends-drift-further` (from F6, F2): While a coin's 50-day SMA is above its 200-day SMA, the coin's upward drift is larger the higher its recent daily volatility.
- `002-01_sma-golden-cross-upward-drift.d4_recent-rise-keeps-rising` (from F2, F5): After a coin has risen strongly over its recent weeks, it keeps rising over the following days, and the larger the past rise, the larger the next rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
