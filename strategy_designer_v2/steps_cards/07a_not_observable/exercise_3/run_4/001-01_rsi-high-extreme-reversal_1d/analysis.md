---
line: 7.a not observable
backtest: 001-01_rsi-high-extreme-reversal_1d
idea tested: 001-01_rsi-high-extreme-reversal
step 5: not observable
step 6: none
mode: one call
explorations: 1
cost: 0.1611 USD
---
## Findings
- **F1:** The backtest ran on one coin and one window only: BTCUSD w1, 120 daily bars, all in 2022. ETH and BNB are absent, so the plan's rule of "negative in at least 2 of 3 coins" could not be met by construction.
- **F2:** The high-extreme situation is not rare on the bars: the forecast is −10 or lower on 15 of 120 bars (12.5 %), and below 0 on 32.5 %. These extreme bars cluster into only 3 runs, of 1, 2 and 12 bars, so the 5-bar grid (23 usable cases) catches only 3 independent extreme cases, against the plan's minimum of 30.
- **F3:** The config reaches the extreme easily, because the 60-bar standardisation saturates the forecast at moderate RSI. RSI(14) between 60 and 65 already gives a mean forecast of −15.4 (13 bars, min −20), and 65–75 gives −20 on all 4 bars. RSI above 70 occurred on only 0.8 % of bars. The situation is therefore limited by the short sample, not by the config.
- **F4:** The outcome varies widely from case to case. The three extreme excess 5-bar returns are −0.133, −0.007 and −0.063, with a pooled mean of −0.0675 and t of −1.84 (n=3), which implies a case-to-case standard deviation of about 0.064. The 5-bar return over all grid bars has a standard deviation of 0.076, so a realistic effect of about 1 % per 5 days would need about (2×0.076/0.01)² ≈ 230 cases.
- **F5:** At the observed rate of about 3 independent extreme cases per 120-bar coin-window, 30 cases need about 10 coin-windows. That is well within the default data: 6 coins, each across the windows of all four folds.

## Ideas
- `001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample` (from F1, F2, F3, F4, F5): After the relative strength index reaches a high extreme on BTC, ETH or BNB, price falls back over the following bars, giving back part of the preceding rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
