---
line: 7.b inconclusive
backtest: 010-01_rsi-above-share-continuation.g1_rsi-share-continuation-calm-markets_1d
idea tested: 010-01_rsi-above-share-continuation.g1_rsi-share-continuation-calm-markets
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.2964 USD
---
## Findings
- **F1:** The tested slope is essentially zero at the plan's horizon, with a pooled t of 0.004 and a correlation of 0.0003 over 191 non-overlapping 14-day cases. It is also near zero at the neighbouring horizons, with t 0.98 at 7 days (n=414) and t 0.68 at 30 days (n=88).
- **F2:** The effect is absent in both coins and mixed across years. The 14-day slope t is -0.31 for BTC (n=96) and 0.23 for ETH (n=95). Six of the eight years have a negative slope, from 2018 at -1.40 to 2023 at -1.66, with 2020 at -2.08. Only 2019 (0.61), 2024 (0.33) and 2025 (1.28) are positive, so the yearly signs cancel.
- **F3:** Neither the side nor the strength of the forecast shows the idea. On the 14-day grid, long-side bars had a demeaned return of -0.0015 (n=93) and short-side bars -0.0129 (n=98). The signed return by forecast-size tercile goes 0.009, 0.028 and then -0.020, so the largest forecasts do worst.
- **F4:** The volatility condition does not bring the effect out. The raw RSI share has a 14-day slope t of 0.43 in the calm regime (n=101) and -0.32 outside it (n=91). By volatility-rank tercile it is 0.57, -1.72 and -0.37, with no gradient.
- **F5:** The RSI level itself, not the share of days above 50, carries the only clear sign, and only in the calm regime. In calm bars the 7-day forward return rises with the 14-day RSI (t 2.52, n=368), compared with t -0.35 (n=351) in high-volatility bars. In calm bars the same slope is t 1.04 at 14 days and t 1.67 at 30 days. The coin's 30-day return points the same way at 7 days in calm bars (t 1.77, n=303).
- **F6:** The result is a zero, not a small effect short of the bar. Step 6's positive timing part (0.00106) comes with a book that earns less than holding (Sharpe minus holding's Sharpe -0.031). BNB is not in the available data, and the slope is flat in both coins tested, so more of the same data would not move a t of 0.004.

## Ideas
- `010-01_rsi-above-share-continuation.g1_rsi-share-continuation-calm-markets.b1_calm-market-rsi-level-continuation` (from F5, F4, F1): The higher a coin's 14-day RSI at the close, the higher its return over the next 7 days, while the coin's 30-day volatility of daily returns is low relative to its own history.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
