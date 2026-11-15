---
line: 7.b inconclusive
backtest: 002-01_sma-golden-cross-upward-drift_1d
idea tested: 002-01_sma-golden-cross-upward-drift
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.2875 USD
---
## Findings
- **F1:** The 50/200 SMA spread forecast does not grade forward returns at any horizon. The pooled slope t is 0.61, 0.21, 0.20, 0.37, 0.55 and −0.06 at 1, 3, 5, 10, 20 and 40 bars. At 10 bars the on-minus-off excess return is +0.0005 vs −0.0005 (Welch t 0.14, 832 vs 825 blocks). The result is unclear because the spread's size carries nothing, not because the sample is small.
- **F2:** The size of the spread is non-monotonic. Mean 10-bar excess by forecast bucket runs +0.004 (0–2), −0.017 (2–5), +0.012 (5–8), −0.008 (8–12) and +0.006 (12–20). By raw-spread octile it alternates sign, with t between −1.6 and +1.9.
- **F3:** The effect is mixed across coins and years. Per-coin slope t runs from −0.28 (XRP) to 0.94 (BTC). The on-minus-off t is negative in 2020 (−2.56), 2022 (−1.68) and 2023 (−1.94) and positive only in 2025 (+0.46).
- **F4:** Inside the up-cross state, the coin's own recent move grades what follows. Regressing the 10-bar excess return on the past 20-bar return gives slope 0.069, t 3.26 (694 blocks). On the past 10-bar return it gives slope 0.123, t 3.53 (762 blocks). In the down-cross state the same slopes are flat: t −0.84 and −0.12 (681 and 754 blocks).
- **F5:** Within the up-cross state, the top quartile of past 20-bar return beats the bottom quartile by 0.063 in 10-bar excess return (Welch t 2.95, 174 vs 174 blocks). The bottom quartile alone averages −0.033 (t −2.96). The top quartile alone averages +0.036 (t 2.02).
- **F6:** Within the up-cross state, price sitting below its 50-day SMA is followed by losses. The lowest quartile of close/SMA50 averages −0.049 in 10-bar excess return (t −4.22, 124 blocks), against +0.020 in the third quartile (t 1.13).
- **F7:** The momentum grading inside the up-cross state is not uniform across years. Its slope t is positive in 2024 (2.47) and 2025 (2.24) but negative in 2022 (−2.16, 14 blocks) and 2023 (−2.66). Its sign is positive for four of six coins (t up to 1.78 for ZEC).

## Ideas
- `002-01_sma-golden-cross-upward-drift.b1_momentum-inside-golden-cross` (from F1, F4, F5, F7): While a coin's short moving average of close is above its long one, the coin's forward return over the following days is larger the stronger its own rise over the preceding weeks has been, and it falls further the deeper its recent drop.
- `002-01_sma-golden-cross-upward-drift.b2_break-below-short-average` (from F2, F6): While a coin's short moving average of close is above its long one, the further its close sits below its short moving average, the more it falls over the following days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
