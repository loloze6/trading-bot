---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-01_sma-golden-cross-upward-drift
line: 7.b inconclusive
backtest: 002-01_sma-golden-cross-upward-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: After the 50-day SMA crosses below the 200-day SMA, the coin rises over the following weeks by more than its usual return, the more so the more recently the cross happened.
Consequence: A trader would treat a fresh death cross as a rebound opportunity rather than a signal to sell.
Why:
- F4: Fresh crosses go against the brief on both sides. In the first 20 bars after an up-cross, the 10-bar excess return is −0.018 (n 107, t ≈ −1.4). In the first 20 bars after a down-cross it is +0.019 (n 96, t ≈ 1.4), and +0.024 between 20 and 60 bars after (n 100, t ≈ 1.8). Strong rebounds below the 200-day line offset the up-state gain.
- F5: The effect splits by coin and by year. On minus off at 10 bars is +0.014 for ETH (t 0.80) and −0.016 for LTC (t −0.90), and it is negative in 6 of 8 years: 2020 gives 0.0088 vs 0.0610 (t −2.56) and 2023 gives −0.0087 vs 0.0185 (t −1.94). The pooled slope therefore averages opposite signs.
