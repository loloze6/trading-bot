---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.b inconclusive
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's close sits above its 200-day simple moving average, the further above it sits, the more the coin rises over the next 20 days compared with its usual 20-day move, only while the coin's 60-day volatility of daily returns is low compared with its own past.
Consequence: If confirmed, a trader would follow the trend above the 200-day average only in calm conditions and stand aside when volatility is high.
Why:
- F6: Volatility splits the effect, but not significantly. Above-average bars in the lowest third of 60-day volatility earn +0.022 (t 1.12, n 86), against +0.003 (mid, n 46) and −0.007 (high, n 64), with a hit rate of 0.36 in high volatility. The vol-target sizing puts 0.87 allocation in low volatility versus 0.36 in high, which is part of why the weighted measure reached t 1.73.
- F5: Two bear years drag it down. Forecast > 0 bars in 2018 (−0.132, t −2.76, n 21) and 2022 (−0.173, t −3.12, n 10) lose heavily, while 2019-2021 and 2023-2025 sit between −0.003 and +0.036 with t below 0.9.
- F1: The forecast's grading only half shows at 20 days. Excess returns over 20 x the coin's mean daily return rise with the forecast: 0-5 gives −0.029 (t −1.63, n 111), 5-10 gives −0.011 (t −0.54, n 100), 10-15 gives +0.002 (t 0.08, n 75) and 15-20 gives +0.055 (t 1.17, n 113). But the Spearman correlation of forecast with excess is only 0.043 (n 399), and it is 0.018 to 0.060 at 5, 10, 40 and 60 days, so no horizon shows a clear effect.
