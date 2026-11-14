---
line: 7.a not observable
backtest: 001-01_rsi-high-extreme-reversal_1d
idea tested: 001-01_rsi-high-extreme-reversal
step 5: not observable
step 6: none
mode: one call
explorations: 2
cost: 0.2356 USD
---
## Findings
- **F1:** The backtest holds only BTCUSD in a single window w1 of 120 daily bars (119 days), not the brief's three coins. That gives only 23 non-overlapping 5-bar blocks in total, so even if every block were extreme it could not reach the plan's minimum of 30 cases.
- **F2:** The forecast reached −10 or lower on 15 of 120 bars (12.5%), grouped into 3 episodes, which left only 3 grid cases against the 30 required. At that share, 30 non-overlapping cases would need about 1200 daily bars per coin, roughly 3.3 years.
- **F3:** The component's logged RSI never exceeded 58.0 (median 47.5, 95th percentile 55.2, 0 bars above 60 or 70), and the bars with forecast ≤ −10 had RSI between 54.0 and 58.0 (mean 55.6). The "high extreme" was therefore only high relative to the 60-bar standardisation, not an absolute extreme. A Wilder RSI(14) recomputed on the closes ranged from 11.9 to 70.1.
- **F4:** The direction leaned towards reversal but was underpowered. The 3 grid cases had excess 5-bar returns of −13.3%, −0.7% and −6.3% (mean −6.75%, t −1.84). The 15 overlapping extreme bars averaged −2.3% (std 5.7%, t −1.60), and about 23 independent cases would give t = −2 at that effect size, because the 5-bar forward return std is 7.3%.
- **F5:** The excess return deepened as the forecast grew more negative: −1.3% (t −1.15, n 39) for any short reading, −1.6% (t −1.33) at ≤ −1, −2.7% (t −1.73, n 23) at ≤ −5. This happened in a window where BTC fell 21.1% and the 5-bar baseline was −0.5%.

## Ideas
- `001-01_rsi-high-extreme-reversal.a1_relative-high-rsi-daily-reversal` (from F1, F2, F4, F5): When a coin's RSI(14) on daily bars is high relative to its own previous 60 readings, its return over the next 5 bars is below its average 5-bar return, observed on each of BTC, ETH and BNB over several years of daily bars.
- `001-01_rsi-high-extreme-reversal.a2_relative-high-rsi-intraday-reversal` (from F2, F3, F4): When a coin's RSI(14) on 4-hour bars is high relative to its own previous 60 readings, its return over the next 5 bars is below its average 5-bar return.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
