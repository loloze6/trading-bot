---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-01_sma-golden-cross-upward-drift
line: 7.b inconclusive
backtest: 002-01_sma-golden-cross-upward-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's short moving average of close is above its long one, the coin's forward return over the following days is larger the stronger its own rise over the preceding weeks has been, and it falls further the deeper its recent drop.
Consequence: A trader would size longs in an up-cross trend by the coin's recent momentum and step aside when price has been falling despite the averages still pointing up.
Why:
- F1: The 50/200 SMA spread forecast does not grade forward returns at any horizon. The pooled slope t is 0.61, 0.21, 0.20, 0.37, 0.55 and −0.06 at 1, 3, 5, 10, 20 and 40 bars. At 10 bars the on-minus-off excess return is +0.0005 vs −0.0005 (Welch t 0.14, 832 vs 825 blocks). The result is unclear because the spread's size carries nothing, not because the sample is small.
- F4: Inside the up-cross state, the coin's own recent move grades what follows. Regressing the 10-bar excess return on the past 20-bar return gives slope 0.069, t 3.26 (694 blocks). On the past 10-bar return it gives slope 0.123, t 3.53 (762 blocks). In the down-cross state the same slopes are flat: t −0.84 and −0.12 (681 and 754 blocks).
- F5: Within the up-cross state, the top quartile of past 20-bar return beats the bottom quartile by 0.063 in 10-bar excess return (Welch t 2.95, 174 vs 174 blocks). The bottom quartile alone averages −0.033 (t −2.96). The top quartile alone averages +0.036 (t 2.02).
- F7: The momentum grading inside the up-cross state is not uniform across years. Its slope t is positive in 2024 (2.47) and 2025 (2.24) but negative in 2022 (−2.16, 14 blocks) and 2023 (−2.66). Its sign is positive for four of six coins (t up to 1.78 for ZEC).
