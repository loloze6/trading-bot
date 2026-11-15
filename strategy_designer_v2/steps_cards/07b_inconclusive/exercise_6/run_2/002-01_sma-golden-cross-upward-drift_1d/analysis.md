---
line: 7.b inconclusive
backtest: 002-01_sma-golden-cross-upward-drift_1d
idea tested: 002-01_sma-golden-cross-upward-drift
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3393 USD
---
## Findings
- **F1:** The tested slope is near zero at every horizon, not only the plan's: 0.000202 with t 0.37 at 10 days (1657 non-overlapping blocks, 832 with forecast > 0); t 0.20 at 5 days (3349 blocks), 0.55 at 20 days (811) and 0.09 at 30 days (529); on forecast > 0 blocks alone the slope is t 0.37 (832).
- **F2:** The effect is not graded by the spread. The mean 10-day excess return by forecast bucket runs -0.0085 (0–5, n 212), 0.0023 (5–10, n 183), 0.0105 (10–15, n 174) and 0.00004 (15–20, n 263), with a standard deviation of 0.15–0.22 in each bucket. The hit rates in the positive buckets (0.47–0.52) are below the flat bucket's 0.53, which matches the failed supporting check (-0.021).
- **F3:** The result is mixed across coins. The per-coin t runs from -0.28 (XRP) to 0.94 (BTC), and the mean excess return on forecast > 0 blocks is positive for ETH (0.0063), ZEC (0.0073) and BTC (0.0024) but negative for LTC (-0.0086), XRP (-0.0046) and XMR (-0.0011).
- **F4:** The forecast mostly tracks the market's yearly move rather than predicting the next 10 days.
- **F5:** The coin's own past 10-day return predicts its next 10-day excess return where the spread does not.
- **F6:** Time since the up-cross does not grade the move either: slope t 0.47 (274 blocks), and the age buckets alternate in sign (0.0038, -0.037, 0.019, -0.013).

## Ideas
- `002-01_sma-golden-cross-upward-drift.b1_golden-cross-spread-drift` (from F1, F3): While a coin's 50-day SMA is above its 200-day SMA, the wider the percent spread between the two, the more the coin rises over the next 10 days relative to its usual 10-day return.
- `002-01_sma-golden-cross-upward-drift.b2_uptrend-short-term-momentum-continuation` (from F5, F4, F2): While a coin's 50-day SMA is above its 200-day SMA, the larger the coin's 10-day return, the more it rises over the next 10 days relative to its usual 10-day return.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
