---
line: 7.b inconclusive
backtest: 002-03_price-cross-above-long-sma_1d
idea tested: 002-03_price-cross-above-long-sma
step 5: inconclusive
step 6: not profitable enough
mode: analyst then deducer
explorations: 2
cost: 0.3329 USD
---
## Findings
- **F1:** The positive block mean comes from a few extreme blocks: the top 10 of 499 active blocks hold 183% of the total P&L, only 37.3% of blocks are positive (median -0.18), and t drops from 1.25 to 0.60 after 1% winsorising, to -0.74 without the top 5 blocks, and to -1.96 without the top 10.
- **F2:** On the 7046 active bars the typical outcome is a loss against holding: median 20-bar excess return -0.031 against a mean of +0.0065, standard deviation 0.298, maximum +4.57, and only 42.0% of bars beat the coin's drift.
- **F3:** The effect sits in the largest forecasts only: the top forecast quintile (close about 88% above the 200-day SMA, forecast near the 20 cap) has mean excess +0.052, against -0.027 and -0.023 in the two lowest quintiles; blocks in the lowest third of mean forecast lose -0.18 with t -5.09, while the highest third gain +1.27 with t 1.70.
- **F4:** Measured against the cross-coin average 20-bar return, the forecast adds nothing overall (relative return -0.001 when on vs +0.001 when off); only the top quintile beats the other coins (+0.039 mean, 49.0% hit), while quintiles 0 to 3 all trail them (-0.007 to -0.016).
- **F5:** In the top forecast quintile the result splits by coin: BTC is the only coin with a clean edge (mean +0.063, median +0.027, 58.5% hit); ZEC's +0.215 mean rests on tails (median -0.026); XRP (23.8% hit, median -0.129) and XMR (32.7% hit, mean -0.040) lose.
- **F6:** The result swings by period and goes both ways: windows w11 (+4.62, t 3.24), w17 (+2.14, t 2.56) and w10 (t 2.26) are strongly positive, while w13 (-2.64, t -3.47), w16 (-2.61, t -3.14), w18 (-3.02, t -2.80), w12 (t -2.49) and w22 (t -2.38) are strongly negative; the top quintile earns +0.267 in 2025 but -0.064 in 2023 and -0.039 in 2019.
- **F7:** The first 20 bars after the close moves above the SMA, which is the cross itself, underperform (mean excess -0.015, 40.8% hit, n 3030); bars 60 to 120 days into the run do better (mean +0.035, 45.6% hit, n 1315).
- **F8:** Active bars whose coin fell over the trailing 60 days (bottom quartile, mean -7%) lose (mean excess -0.016, 32.6% hit); bars after a moderate +16% trailing rise do best (mean +0.058, 49.1% hit), and after a +115% rise the edge fades (mean +0.034, 42.8% hit).
- **F9:** For XRP, being above the SMA is worse than being below it: 27.0% of on-bars beat drift against 46.3% of off-bars, with a median on-bar excess of -0.083.

## Ideas
- `002-03_price-cross-above-long-sma.b1_extreme-distance-above-sma` (from F3, F4): When a coin's close sits far above its 200-day SMA, at the top of its own recent range of distances, the coin keeps rising over the next 20 bars more than its usual drift.
- `002-03_price-cross-above-long-sma.b2_mature-run-above-sma` (from F7): When a coin's close has stayed above its 200-day SMA for 60 to 120 days in a row, the coin keeps rising over the next 20 bars more than its usual drift.
- `002-03_price-cross-above-long-sma.b3_fresh-cross-underperforms-drift` (from F7): When a coin's close has just moved above its 200-day SMA within the last 20 bars, the coin rises less than its usual drift over the next 20 bars.
- `002-03_price-cross-above-long-sma.b4_moderate-prior-rise-continuation` (from F8): When a coin's close is above its 200-day SMA and the coin has risen moderately over the trailing 60 days (around +10% to +30%), the coin keeps rising over the next 20 bars more than its usual drift.
- `002-03_price-cross-above-long-sma.b5_above-sma-after-decline` (from F8, F2): When a coin's close is above its 200-day SMA but the coin has fallen over the trailing 60 days, the coin rises less than its usual drift over the next 20 bars.
- `002-03_price-cross-above-long-sma.b6_btc-extreme-distance-trend` (from F5, F3): When BTC's close is far above its 200-day SMA, at the top of its own recent range of distances, BTC keeps rising over the next 20 bars more than its usual drift on most such bars.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
