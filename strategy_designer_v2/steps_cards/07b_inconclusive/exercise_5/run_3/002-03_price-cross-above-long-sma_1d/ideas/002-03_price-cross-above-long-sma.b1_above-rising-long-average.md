---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.b inconclusive
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's close is above its 200-day simple moving average, the further it sits above, the more it rises beyond its usual drift over the next 20 days, only while that 200-day average has itself risen over the past 20 days.
Consequence: A trader should follow a close above the long average only when the average is rising, and should refuse that long when the average is falling, as in 2018 and 2022.
Why:
- F2: The rising or falling of the 200-day average splits the active bars into two opposite groups: with the average up over the past 20 days the next-20-day excess is +0.026 (t 1.17, n 266), with it down it is −0.037 (t −2.03, n 133); over all bars the excess climbs from −0.020 in the steepest-falling slope quintile to +0.034 and +0.019 in the two rising quintiles (n 134 each).
- F3: The result is a mix of opposite years: active bars lost in 2018 (−0.132, t −2.76, n 21) and 2022 (−0.173, t −3.12, n 10), which were falling-average bear years, while blocks earned in 2020 (+0.46, t 2.03) and were positive in 2024 and 2025 (+0.36 and +0.31).
- F4: Being above the average does not carry the effect, and fresh crosses do not continue: raw-distance quintiles at 20 days are flat (+0.002, +0.004, −0.007, +0.008, +0.006, all |t| < 0.5), and active bars in the first 20 days after a cross average −0.008 (n 95) and 20–60 days −0.020 (n 62), so the plan's "after the cross" situation shows nothing.
